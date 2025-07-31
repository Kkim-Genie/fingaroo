from app.agent.states.basic_state import GraphState
from app.agent.tools.dart.economy import financial_statement_tool, multi_company_account_tool, single_company_account_tool, single_financial_indicator_tool
from app.agent.tools.dart.principal import changed_capital_tool, multi_financial_indicator_tool, total_stock_tool, treasury_stock_tool
from app.invest_log.application.invest_log_service import InvestLogService
from app.invest_log.infra.repository.invest_log_repo import InvestLogRepository
from langchain_core.messages import ToolMessage, ToolCall
import json
import uuid
from app.dart.infra.repository.corp_code_repo import DartCorpCodeRepository
from app.dart.application.corp_code_service import DartCorpCodeService
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_naver import ChatClovaX
from app.config import get_settings
import requests
import traceback

from app.knowledge.application.embeddings_service import EmbeddingsService
from app.knowledge.infra.repository.embeddings_repo import EmbeddingsRepository
from app.stock_price.application.stock_price_service import StockPriceService

settings = get_settings()


system_prompt = f"""
    당신은 분석할 회사를 선정하는 agent입니다. 회사명을 기준으로 검색을 시행합니다.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "위 대화를 참고하여 분석할 회사명을 알려주세요."
        ),
    ]
)

def find_corp_code_node(state: GraphState):
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
                    "company_name": {
                        "type": "string",
                        "description": "주식 가격을 조회할 회사명",
                    }
                }
            },
            "required": ["company_name"]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_data = response.json()
        content = result_data["result"]["message"]["content"]
        
        # JSON 파싱하여 RouteResponse 객체 생성
        parsed_content = json.loads(content)
        company_name = parsed_content["company_name"]

        corp_code_repo = DartCorpCodeRepository()
        corp_code_service = DartCorpCodeService(corp_code_repo=corp_code_repo)
        corp_code = corp_code_service.find_by_corp_name(company_name)

        tool_message = ToolMessage(
            name="find_corp_code",
            content=f"회사명: {corp_code.corp_name}, 종목코드: {corp_code.corp_code}",
            tool_call_id=str(uuid.uuid4()),
        )
        print("corp_code: ", corp_code)

        return {
            "messages": state["messages"] + [tool_message],
            "analysis_corp_code": corp_code.corp_code
        }
        
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
        return


query_system_prompt = f"""
    당신은 회사를 분석하기 위한 정보를 검색하기 위한 query를 작성하는 agent입니다.
"""

query_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", query_system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "위 대화를 참고하여 분석할 회사의 정보를 검색하기 위한 하나의 query를 작성해주세요."
        ),
    ]
)

def company_analysis_query_write_node(state: GraphState):
    llm = ChatClovaX(
        model=settings.LLM_MODEL_BASE, 
        api_key=settings.CLOVASTUDIO_API_KEY
    )
    chain = query_prompt | llm
    answer = chain.invoke(state)

    tool_message = ToolMessage(
        content = answer.content,
        tool_call_id=str(uuid.uuid4()),
    )
    print("analysis_query: ", answer.content)

    return {
        "messages": state["messages"] + [tool_message],
        "analysis_query": answer.content
    }

route_system_prompt = f"""
    당신을 회사를 분석하기 위한 도구를 선택하는 agent입니다.
    당신이 사용할 수 있는 도구는 [search_knowledge_base, search_stock_price, search_dart] 입니다.
    당신은 회사를 분석하기 위한 도구를 선택해야 합니다.

    선택 우선순위는 search_stock_price -> search_dart -> search_knowledge_base 입니다.

    search_knowledge_base: 여러 경제 뉴스에 기반한 지식 베이스에서 검색
    search_stock_price: 주식 가격을 조회
    search_dart: 공시 정보를 조회
        검색 가능한 공시 정보
        1. 단일회사 계정정보(get_single_company_account)
        2. 다중회사 계정정보(get_multi_company_account)
        3. 단일회사 재무제표(get_single_financial_indicator)
        4. 다중회사 재무제표(get_multi_financial_indicator)
        5. 재무정보 (get_financial_statement)
        6. 자본금 변화(get_changed_capital)
        7. 전환사채 발행 정보(get_treasury_stock)
        8. 총 주식 수(get_total_stock)

    당신은 회사를 분석하기 위한 도구를 선택해야 합니다.
"""

route_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", route_system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "위 대화를 참고하여 [search_knowledge_base, search_stock_price, search_dart] 중 하나를 선택해주세요."
        ),
    ]
)
def company_analysis_route_node(state: GraphState):
    formatted_prompt = route_prompt.format(messages=state["messages"])

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
                    "tool_name": {
                        "type": "string",
                        "description": "회사를 분석하기 위한 도구 이름",
                        "enum": ["search_knowledge_base", "search_stock_price", "search_dart"]
                    }
                }
            },
            "required": ["tool_name"]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_data = response.json()
        content = result_data["result"]["message"]["content"]
        
        # JSON 파싱하여 RouteResponse 객체 생성
        parsed_content = json.loads(content)
        tool_name = parsed_content["tool_name"]
        print("next_tool", tool_name)

        return {
            "next": tool_name
        }

        
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
        return

async def search_company_knowledge_base_node(state: GraphState):
    print("search knowledge_base")
    query = state["analysis_query"]
    embeddings_repo = EmbeddingsRepository()
    embeddings_service = EmbeddingsService(embeddings_repo=embeddings_repo)
    searched = await embeddings_service.retrieve_by_query(query, 5)
    content = ""
    for embedding in searched:
        content += embedding.content + "\n"
    tool_message = ToolMessage(content=content, name="search_knowledge_base", tool_call_id=str(uuid.uuid4()))
    return {"messages": state["messages"] + [tool_message]}

async def search_stock_price_node(state: GraphState):
    print("search stock price")
    corp_code_repo = DartCorpCodeRepository()
    corp_code_service = DartCorpCodeService(corp_code_repo=corp_code_repo)
    stock_price_service = StockPriceService(corp_code_service=corp_code_service)
    stock_price = await stock_price_service.get_by_corp_code(state["analysis_corp_code"])

    tool_message = ToolMessage(
        name="search_stock_price",
        content=stock_price.model_dump_json(),
        tool_call_id=str(uuid.uuid4()),
    )

    return {
        "messages": state["messages"] + [tool_message]
    }


dart_list = [
    "get_single_company_account",
    "get_multi_company_account",
    "get_single_financial_indicator",
    "get_multi_financial_indicator",
    "get_financial_statement",
    "get_changed_capital",
    "get_treasury_stock",
    "get_total_stock",
]
dart_system_prompt = f"""
    당신을 회사를 분석하기 위한 공시 정보를 검색하는 agent입니다.
    당신은 회사를 분석하기 위한 공시 정보를 검색해야 합니다.

    검색 가능한 공시 정보
    1. 단일회사 계정정보(get_single_company_account)
    2. 다중회사 계정정보(get_multi_company_account)
    3. 단일회사 재무제표(get_single_financial_indicator)
    4. 다중회사 재무제표(get_multi_financial_indicator)
    5. 재무정보 (get_financial_statement)
    6. 자본금 변화(get_changed_capital)
    7. 전환사채 발행 정보(get_treasury_stock)
    8. 총 주식 수(get_total_stock)

    당신은 회사를 분석하기 위한 공시 정보를 검색해야 합니다.
"""

dart_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", dart_system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "위 대화를 참고하여 필요한 공시정보를 툴을 이용하여 검색하고 내용을 반환해주세요."
        ),
    ]
)

tools = [
    single_company_account_tool,
    multi_company_account_tool,
    single_financial_indicator_tool,
    multi_financial_indicator_tool,
    financial_statement_tool,
    changed_capital_tool, 
    treasury_stock_tool,
    total_stock_tool,
]
def search_dart_node(state: GraphState):
    print("search_dart_node")
    llm = ChatClovaX(
        model=settings.LLM_MODEL_BASE, 
        api_key=settings.CLOVASTUDIO_API_KEY
    )
    llm.bind_tools(dart_list)
    chain = dart_prompt | llm
    answer = chain.invoke(state)
    tool_message = ToolMessage(
        name="search_dart",
        content=answer.content,
        tool_call_id=str(uuid.uuid4()),
    )

    return {
        "messages": state["messages"] + [tool_message]
    }
    


relevent_system_prompt = f"""
    당신은 검색한 내용이 유저의 질문에 답변하기 충분한지를 확인하는 agent입니다.
    최소한 한번의 주가 검색은 필수입니다.
    공시 정보를 1개 이상 검색해야 합니다.
"""

relevent_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", route_system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "위 대화를 참고하여 유저에게 제공할 정보가 충분한지 확인해주세요. 충분하다면 yes, 부족하다면 no를 선택해주세요."
        ),
    ]
)
def check_company_search_relevent_node(state: GraphState):
    formatted_prompt = relevent_prompt.format(messages=state["messages"])
    
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
                    "answer": {
                        "type": "string",
                        "description": "유저에게 제공할 정보가 충분한지 확인해주세요. 충분하다면 yes, 부족하다면 no를 선택해주세요.",
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
        
        # JSON 파싱하여 RouteResponse 객체 생성
        parsed_content = json.loads(content)
        answer = parsed_content["answer"]
        print("is relevent", answer)

        return {
            "next": answer
        }
        
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
        return {"next": "yes"}