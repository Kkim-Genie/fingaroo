from app.agent.states.basic_state import GraphState
from app.config import get_settings
import requests
import json
import traceback
from langchain_core.messages import ToolMessage, ToolCall
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.dart.application.corp_code_service import DartCorpCodeService
from app.stock_price.application.stock_price_service import StockPriceService
from app.dart.infra.repository.corp_code_repo import DartCorpCodeRepository
import uuid

settings = get_settings()

system_prompt = f"""
    당신은 주식 가격을 조회하는 agent입니다. 회사명을 기준으로 검색을 시행합니다.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "위 대화를 참고하여 주식 가격을 조회할 회사명을 알려주세요."
        ),
    ]
)

def stock_price_agent(state: GraphState):
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
        stock_price_service = StockPriceService(corp_code_service=corp_code_service)
        stock_price = stock_price_service.get_by_corp_name(company_name)

        tool_message = ToolMessage(
            name="search_stock_price",
            content=stock_price.model_dump_json(),
            tool_call_id=str(uuid.uuid4()),
            tool_calls=[ToolCall(
                name="search_stock_price",
                args={"name": company_name}
            )]
        )

        return {
            "messages": state["messages"] + [tool_message]
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
        return {"next": "FINISH"}