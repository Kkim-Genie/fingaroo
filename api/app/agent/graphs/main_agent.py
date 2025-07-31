from pydantic import BaseModel
from typing import Literal
from app.agent.states.basic_state import GraphState
from app.agent.graphs.search_agent import search_routing_agent, search_news_node, search_daily_report_node, search_knowledge_base_node, generate_search_result_answer_node, check_search_answer_relevent_node, search_query_rewrite_node
from app.agent.graphs.dart_agent import dart_agent
from app.agent.graphs.answer_agent import answer_agent
from app.agent.graphs.stock_price_agent import stock_price_agent
from app.agent.graphs.invest_log_agent import invest_log_agent, invest_read_node, invest_create_node, invest_update_node, invest_delete_node
from app.agent.graphs.invest_feedback_agent import invest_feedback_agent, load_invest_log_node, load_price_node
from app.config import get_settings
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langgraph.graph import END, StateGraph, START
import requests
import json
import traceback

settings = get_settings()
checkpointer = MemorySaver()

members = [
    "dart_agent",
    "stock_price_agent",
]
options_for_next = ["answer_agent", "search_routing_agent", "invest_log_agent", "invest_feedback_agent"] + members

system_prompt = f"""
    You are a supervisor tasked with managing a conversation between the
    following workers:  {members}. Given the following user request,
    respond with the worker to act next. Each worker will perform a
    task and respond with their results and status. 
    When finished or there is no need to call any worker, respond with *answer_agent*.

    추가 worker 설명
    search_routing_agent: 경제 관련 데이터를 검색하는 agent입니다. 뉴스와 시황, 그리고 지식베이스에서 검색을 포함합니다.
    stock_price_agent: 주식 가격을 검색하는 agent입니다.
    invest_log_agent: 매매일지를 관리하는 agent입니다.
    invest_feedback_agent: 매매일지를 기반으로 피드백을 제공하는 agent입니다.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "Given the conversation above, who should act next? "
            "Or should we FINISH? Select one of: {options}",
        ),
    ]
).partial(options=str(options_for_next), members=", ".join(members))

class RouteResponse(BaseModel):
    next: Literal[*options_for_next]

def supervisor(state: GraphState):
    formatted_prompt = prompt.format(messages=state["messages"])
    
    
    # CLOVA Studio v3 API 직접 호출
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
                    "next": {
                        "type": "string",
                        "description": "The next agent to call",
                        "enum": options_for_next
                    }
                }
            },
            "required": ["next"]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_data = response.json()
        content = result_data["result"]["message"]["content"]
        print(content)
        
        # JSON 파싱하여 RouteResponse 객체 생성
        parsed_content = json.loads(content)
        route_response = RouteResponse(**parsed_content)
        
        return {"next": route_response.next}
        
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
        return {"next": "FINISH"}

def main_agent():
    workflow = StateGraph(GraphState)

    workflow.add_node("Supervisor", supervisor)
    workflow.add_node("search_routing_agent", search_routing_agent)
    workflow.add_node("dart_agent", dart_agent)
    workflow.add_node("answer_agent", answer_agent)
    workflow.add_node("stock_price_agent", stock_price_agent)

    workflow.add_node("search_news_node", search_news_node)
    workflow.add_node("search_daily_report_node", search_daily_report_node)
    workflow.add_node("search_knowledge_base_node", search_knowledge_base_node)

    workflow.add_node("generate_search_result_answer_node", generate_search_result_answer_node)
    workflow.add_node("check_search_answer_relevent_node", check_search_answer_relevent_node)
    workflow.add_node("search_query_rewrite_node", search_query_rewrite_node)

    workflow.add_node("invest_log_agent", invest_log_agent)
    workflow.add_node("invest_read_node", invest_read_node)
    workflow.add_node("invest_create_node", invest_create_node)
    workflow.add_node("invest_update_node", invest_update_node)
    workflow.add_node("invest_delete_node", invest_delete_node)

    workflow.add_node("load_invest_log_node", load_invest_log_node)
    workflow.add_node("load_price_node", load_price_node)
    workflow.add_node("invest_feedback_agent", invest_feedback_agent)

    for member in members:
        workflow.add_edge(member, "Supervisor")

    conditional_map = {k: k for k in members}
    conditional_map["answer_agent"] = "answer_agent"
    conditional_map["search_routing_agent"] = "search_routing_agent"
    conditional_map["invest_log_agent"] = "invest_log_agent"
    conditional_map["invest_feedback_agent"] = "load_invest_log_node"

    def get_next(state):
        return state["next"]

    workflow.add_conditional_edges("Supervisor", get_next, conditional_map)

    def get_task(state):
        return state["task"]

    workflow.add_conditional_edges("search_routing_agent", get_task, {
        "news": "search_news_node",
        "daily_report": "search_daily_report_node",
        "knowledge_base": "search_knowledge_base_node",
    })

    workflow.add_edge("search_news_node", "generate_search_result_answer_node")
    workflow.add_edge("search_daily_report_node", "generate_search_result_answer_node")
    workflow.add_edge("search_knowledge_base_node", "generate_search_result_answer_node")

    workflow.add_edge("generate_search_result_answer_node", "check_search_answer_relevent_node")

    def get_answer(state):
        return state["answer"]

    workflow.add_conditional_edges("check_search_answer_relevent_node", get_answer, {
        "yes": "Supervisor",
        "no": "search_query_rewrite_node",
    })

    workflow.add_edge("search_query_rewrite_node", "search_routing_agent")

    def get_invest_action(state):
        return state["action"]

    workflow.add_conditional_edges("invest_log_agent", get_invest_action, {
        "read": "invest_read_node",
        "create": "invest_create_node",
        "update": "invest_update_node",
        "delete": "invest_delete_node",
    })

    workflow.add_edge("invest_read_node", "Supervisor")
    workflow.add_edge("invest_create_node", "Supervisor")
    workflow.add_edge("invest_update_node", "Supervisor")
    workflow.add_edge("invest_delete_node", "Supervisor")

    workflow.add_edge(START, "Supervisor")
    workflow.add_edge("answer_agent", END)

    workflow.add_edge("load_invest_log_node", "load_price_node")
    workflow.add_edge("load_price_node", "invest_feedback_agent")
    workflow.add_edge("invest_feedback_agent", "Supervisor")

    graph = workflow.compile(checkpointer=checkpointer)

    return graph

# def test_node(state: GraphState):
#     llm = ChatClovaX(
#         model=settings.LLM_MODEL_BASE, 
#         api_key=settings.CLOVASTUDIO_API_KEY
#     )
#     return llm.invoke(state["messages"])

# def main_agent():
#     workflow = StateGraph(GraphState)

#     workflow.add_node("test_node", test_node)

#     workflow.add_edge(START, "test_node")
#     workflow.add_edge("test_node", END)

#     graph = workflow.compile(checkpointer=MemorySaver())

#     return graph