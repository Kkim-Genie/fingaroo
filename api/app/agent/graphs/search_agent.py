from app.agent.tools.search.naver_search import naver_search
from app.agent.tools.search.search_financial_quote import search_financial_quote
from app.agent.tools.search.search_news import search_news
from app.agent.tools.search.search_daily_report import search_daily_report
from app.agent.tools.search.search_knowledge_base import search_knowledge_base
from langgraph.prebuilt import create_react_agent
from app.config import get_settings
from langchain_naver import ChatClovaX
from datetime import datetime
from langgraph.checkpoint.memory import InMemorySaver
from app.agent.states.basic_state import GraphState
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import requests
import json
import traceback
from pydantic import BaseModel
from typing import Literal
from app.knowledge.application.news_service import NewsService
from app.knowledge.infra.repository.news_repo import NewsRepository
from app.knowledge.infra.repository.embeddings_repo import EmbeddingsRepository
from langchain_core.messages import ToolMessage
from app.utils.langgraph import embedding_string
from langchain.utils.math import cosine_similarity
from app.knowledge.application.embeddings_service import EmbeddingsService
import uuid
import numpy as np
from app.knowledge.application.daily_report_service import DailyReportService
from app.knowledge.infra.repository.daily_report_repo import DailyReportRepository


settings = get_settings()

system_prompt = f"""
    today date is {datetime.now().strftime("%Y-%m-%d")}
    You are an expert at routing a user question to a knowledge_base or news or daily_report(시황).
    News and daily_report need exact date like YYYY-MM-DD. So if there is no date in the question, you should use knowledge_base.
    If you can calculate exact date with the question and today date, you should use the date.
    The knowledge_base contains documents related to economic issues."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "Given the conversation above, who should act next? "
            "Select one of: [knowledge_base, news, daily_report]",
        ),
    ]
)

class RouteResponse(BaseModel):
    task: Literal["knowledge_base", "news", "daily_report"]
    date: str

def search_routing_agent(state: GraphState):
    formatted_prompt = prompt.format(messages=state["messages"])

    url = f"https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-007"

    headers = {
        "Authorization": f"Bearer {settings.CLOVASTUDIO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "user", "content": formatted_prompt}],
        "maxCompletionTokens": 100,
        "temperature": 0.1,
        "thinking": {
          "effort": "none",
        },
        "responseFormat": {
            "type": "json",
            "schema":{
                "type": "object",
                "properties": {
                    "task": {
                        "type": "string",
                        "description": "The next task to call",
                        "enum": ["knowledge_base", "news", "daily_report"]
                    },
                    "date":{
                        "type": "string",
                        "description": "The date to search",
                        "format": "date"
                    }
                }
            },
            "required": ["task", "date"]
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_data = response.json()
        content = result_data["result"]["message"]["content"]
        
        # JSON 파싱하여 RouteResponse 객체 생성
        parsed_content = json.loads(content)
        route_response = RouteResponse(**parsed_content)
        print("next task", route_response.task, "date", route_response.date)
        
        return {"task": route_response.task, "search_date": route_response.date}
        
    except Exception as e:
        print(f"Error calling CLOVA Studio API: {e}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Full traceback:")
        traceback.print_exc()
        
        # HTTP 에러인 경우 응답 정보도 출력
        if hasattr(e, 'response') and e.response is not None:
            print(f"HTTP Status Code: {e.response.status_code}")
            print(f"Response Headers: {e.response.headers}")
            try:
                print(f"Response Content: {e.response.text}")
            except:
                print("Could not decode response content")
        
        # 요청 정보도 출력
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Payload: {json.dumps(payload, indent=2)}")
        
        # 오류 시 기본값 반환
        return {"task": "knowledge_base"}

async def search_news_node(state: GraphState):
    search_date = state["search_date"]
    news_repo = NewsRepository()
    embeddings_repo = EmbeddingsRepository()
    embeddings_service = EmbeddingsService(embeddings_repo=embeddings_repo)
    news_service = NewsService(news_repo=news_repo, embeddings_service=embeddings_service)
    news_list = news_service.find_by_date(search_date)
    query_embedded = await embedding_string(state["query"])

    news_with_similarity = []
    for news in news_list:
        embeded_content = await embedding_string(news.content)
        
        # 1차원 배열을 2차원 배열로 변환
        embeded_content_2d = np.array(embeded_content).reshape(1, -1)
        query_embedded_2d = np.array(query_embedded).reshape(1, -1)
        
        similarity = cosine_similarity(embeded_content_2d, query_embedded_2d)
        news_with_similarity.append({
            "news": news,
            "similarity": similarity[0][0]  # 스칼라 값으로 변환
        })

    news_with_similarity.sort(key=lambda x: x["similarity"], reverse=True)
    news_with_similarity = news_with_similarity[:5]

    content = ""
    for news in news_with_similarity:
        content += f"<document>\n<title>{news['news'].title}</title><date>{news['news'].date}</date>\n<content>{news['news'].content}\n</content/></document>\n"

    tool_message = ToolMessage(content=content, name="search_news", tool_call_id=str(uuid.uuid4()))
    return {"messages": state["messages"] + [tool_message]}

async def search_daily_report_node(state: GraphState):
    search_date = state["search_date"]
    daily_report_repo = DailyReportRepository()
    news_repo = NewsRepository()
    embeddings_repo = EmbeddingsRepository()
    embeddings_service = EmbeddingsService(embeddings_repo=embeddings_repo)
    daily_report_service = DailyReportService(daily_report_repo=daily_report_repo, news_repo=news_repo, embeddings_service=embeddings_service)
    daily_report_list = daily_report_service.find_by_date(search_date)
    target_daily_report = daily_report_list[0]

    content = f"<document>\n<date>{target_daily_report.date}</date>\n<content>{target_daily_report.content}\n</content/></document>\n"

    tool_message = ToolMessage(content=content, name="search_daily_report", tool_call_id=str(uuid.uuid4()))
    return {"messages": state["messages"] + [tool_message]}

async def search_knowledge_base_node(state: GraphState):
    query = state["query"]
    embeddings_repo = EmbeddingsRepository()
    embeddings_service = EmbeddingsService(embeddings_repo=embeddings_repo)
    searched = await embeddings_service.retrieve_by_query(query, 5)
    content = ""
    for embedding in searched:
        content += embedding.content + "\n"
    tool_message = ToolMessage(content=content, name="search_knowledge_base", tool_call_id=str(uuid.uuid4()))
    return {"messages": state["messages"] + [tool_message]}


generate_system_prompt = f"""너는 검색한 내용들을 바탕으로 유저의 질문에 적절한 대답을 만드는 역할을 해."""


def generate_search_result_answer_node(state: GraphState):
    generate_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="messages"),
            (
                "assistant",
                "위의 대화, 특히 마지막 부분의 tool의 결과를 바탕으로 유저의 질문에 적절한 대답을 만드세요."
                "유저의 질문: {query}"
            ),
        ]
    ).partial(query=state["query"])

    llm = ChatClovaX(
        model=settings.LLM_MODEL_BASE, 
        api_key=settings.CLOVASTUDIO_API_KEY,
    )

    chain = generate_prompt | llm
    response = chain.invoke(state)
    tool_message = ToolMessage(content=response.content, name="generate_search_result_answer", tool_call_id=str(uuid.uuid4()))

    return {"messages": state["messages"] + [tool_message]}

check_system = """You are a grader assessing whether an answer addresses / resolves a question \n 
     Give a binary score 'yes' or 'no'. Yes' means that the answer resolves the question."""
check_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", check_system),
        ("human", "User question: \n\n {question} \n\n LLM generation: {generation}"),
    ]
)

class AnswerResponse(BaseModel):
    answer: Literal["yes", "no"]

def check_search_answer_relevent_node(state: GraphState):
    last_message = state["messages"][-1]
    parsed_prompt = check_prompt.partial(question=state["query"], generation=last_message.content)
    
    url = f"https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-007"
    
    headers = {
        "Authorization": f"Bearer {settings.CLOVASTUDIO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "user", "content": parsed_prompt}],
        "maxCompletionTokens": 100,
        "temperature": 0.1,
        "thinking": {
          "effort": "none",
        },
        "responseFormat": {
            "type": "json",
            "schema":{
                "type": "object",
                "properties": {
                    "answer": {
                        "type": "string",
                        "description": "The answer to the question",
                        "enum": ["yes", "no"]
                    }
                }
            },
            "required": ["answer"]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_data = response.json()
        content = result_data["result"]["message"]["content"]
        print("check relevent", content)
        
        # JSON 파싱하여 RouteResponse 객체 생성
        parsed_content = json.loads(content)
        answer_response = AnswerResponse(**parsed_content)
        
        return {"answer": answer_response.answer}
        
    except Exception as e:
        print(f"Error calling CLOVA Studio API: {e}")
        print(f"Exception type: {type(e).__name__}")
        print(f"Full traceback:")
        traceback.print_exc()
        
        # HTTP 에러인 경우 응답 정보도 출력
        if hasattr(e, 'response') and e.response is not None:
            print(f"HTTP Status Code: {e.response.status_code}")
            print(f"Response Headers: {e.response.headers}")
            try:
                print(f"Response Content: {e.response.text}")
            except:
                print("Could not decode response content")
        
        # 요청 정보도 출력
        print(f"Request URL: {url}")
        print(f"Request Headers: {headers}")
        print(f"Request Payload: {json.dumps(payload, indent=2)}")
        
        # 오류 시 기본값 반환
        return {"answer": "no"}

rewrite_system = """You a question re-writer that converts an input question to a better version that is optimized \n 
for vectorstore retrieval. Look at the input and try to reason about the underlying semantic intent / meaning."""
rewrite_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", rewrite_system),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "User question: \n\n {query}\n given above conversation, rewrite the question to be more specific and relevant to the conversation."),
    ]
)

def search_query_rewrite_node(state: GraphState):
    llm = ChatClovaX(
        model=settings.LLM_MODEL_BASE, 
        api_key=settings.CLOVASTUDIO_API_KEY,
    )

    chain = rewrite_prompt | llm
    response = chain.invoke(state)
    rewrited_query = response.content
    print("rewrited query", rewrited_query)
    return {"query": rewrited_query}