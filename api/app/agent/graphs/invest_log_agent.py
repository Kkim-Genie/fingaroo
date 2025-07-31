import json
from datetime import datetime
from langchain_core.messages import ToolCall, ToolMessage
import requests
import traceback
import uuid
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from app.agent.states.basic_state import GraphState
from app.config import get_settings
from app.dart.application.corp_code_service import DartCorpCodeService
from app.dart.infra.repository.corp_code_repo import DartCorpCodeRepository
from app.invest_log.application.user_asset_service import UserAssetService
from app.invest_log.infra.repository.user_asset_repo import UserAssetRepository
from app.invest_log.application.invest_log_service import InvestLogService
from app.invest_log.infra.repository.invest_log_repo import InvestLogRepository
from app.invest_log.domain.invest_log import InvestLog

settings = get_settings()

actions = ["read", "create", "update", "delete"]

system_prompt = f"""
    당신은 매매일지를 관리하는 agent입니다. 아래의 행동 중에서 하나를 선택해야 합니다.
    read: 사용자의 매매일지를 조회
    create: 사용자의 매매일지를 생성
    update: 사용자의 매매일지를 수정
    delete: 사용자의 매매일지를 삭제
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "위 대화를 참고하여 매매일지 관리 행동을 선택해주세요."
        ),
    ]
)

async def invest_log_agent(state: GraphState):
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
                    "action": {
                        "type": "string",
                        "description": "매매일지 관리 행동",
                        "enum": actions
                    }
                }
            },
            "required": ["action"]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_data = response.json()
        content = result_data["result"]["message"]["content"]
        
        # JSON 파싱하여 행동 선택
        parsed_content = json.loads(content)
        action = parsed_content["action"]
        print("action: ", action)

        return {
            "action": action
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
        return {"action": "read"}

def invest_read_node(state: GraphState):
    invest_log_repo = InvestLogRepository()
    invest_log_service = InvestLogService(invest_log_repo=invest_log_repo)
    invest_log = invest_log_service.search_by_user_id(state["user_id"])

    # Convert list of invest logs to JSON
    invest_logs_data = [log.model_dump() for log in invest_log] if invest_log else []
    
    tool_message = ToolMessage(
        name="read_invest_log",
        content=json.dumps(invest_logs_data, ensure_ascii=False, default=str),
        tool_call_id=str(uuid.uuid4()),
        tool_calls=[ToolCall(
            name="read_invest_log",
            args={"user_id": state["user_id"]}
        )]
    )
    return {
        "messages": state["messages"] + [tool_message]
    }

create_log_system_prompt = f"""
    오늘의 날짜: {datetime.now().strftime("%Y-%m-%d")}
    당신은 매매일지를 생성하는 agent입니다. 사용자의 매매일지를 생성해주세요.
    매매일지를 생성하기 위해서는 다음과 같은 정보가 필요합니다.
    date: str, # 매매일
    stock_name: str, # 종목명
    action: str, # 매매 행동(매수|매도)
    amount: int, # 매매 수량
    reason: str, # 매매 이유
    price: int # 매매 가격
"""

create_log_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", create_log_system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "위 대화를 참고하여 각 정보를 정리해 주세요. 만약에 필요한 특정 정보가 없다면 빈 값으로 처리하세요."
        ),
    ]
)

def invest_create_node(state: GraphState):
    formatted_prompt = create_log_prompt.format(messages=state["messages"])
    
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
                    "date": {
                        "type": "string",
                        "format": "date",
                        "description": "매매일"
                    },
                    "stock_name": {
                        "type": "string",
                        "description": "종목명"
                    },
                    "action": {
                        "type": "string",
                        "enum": ["매수", "매도"]
                    },
                    "amount": {
                        "type": "number",
                        "description": "매매 수량"
                    },
                    "reason": {
                        "type": "string",
                        "description": "매매 이유"
                    },
                    "price": {
                        "type": "number",
                        "description": "매매 가격"
                    }
                }
            },
            "required": ["date", "stock_name", "action", "amount", "reason", "price"]
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_data = response.json()
        content = result_data["result"]["message"]["content"]
        
        # JSON 파싱하여 행동 선택
        parsed_content = json.loads(content)
        date = parsed_content.get("date", "")
        stock_name = parsed_content.get("stock_name", "")
        action = parsed_content.get("action", "")
        amount = parsed_content.get("amount", "")
        reason = parsed_content.get("reason", "")
        price = parsed_content.get("price", "")

        need_information = []
        if(date==""):
            need_information.append("date")
        if(stock_name==""):
            need_information.append("stock_name")
        if(action=="" or action not in ["매수", "매도"]):
            need_information.append("action")
        if(amount=="" or amount <= 0):
            need_information.append("amount")
        if(reason==""):
            need_information.append("reason")
        if(price=="" or price <= 0):
            need_information.append("price")

        if(len(need_information) > 0):
            tool_message = ToolMessage(
                name="create_invest_log",
                content=f"필요한 정보가 없습니다. 다음 정보를 입력해주세요: {', '.join(need_information)}\n다음행동: answer_agent를 통해 유저에게 추가 정보를 물어보기",
                tool_call_id=str(uuid.uuid4()),
            )
            return {
                "messages": state["messages"] + [tool_message]
            }

        corp_code_repo = DartCorpCodeRepository()
        dart_corp_code_service = DartCorpCodeService(corp_code_repo=corp_code_repo)
        dart_corp_code = dart_corp_code_service.find_by_corp_name(stock_name)
        if(dart_corp_code is None):
            tool_message = ToolMessage(
                name="create_invest_log",
                content=f"종목명을 찾을 수 없습니다. 다음 정보를 입력해주세요: {stock_name}\n다음행동: answer_agent를 통해 유저에게 추가 정보를 물어보기",
                tool_call_id=str(uuid.uuid4()),
            )
            return {
                "messages": state["messages"] + [tool_message]
            }

        invest_log_repo = InvestLogRepository()
        invest_log_service = InvestLogService(invest_log_repo=invest_log_repo)
        user_asset_repo = UserAssetRepository()
        user_asset_service = UserAssetService(user_asset_repo=user_asset_repo)

        assets = user_asset_service.search_by_user_id(state["user_id"])
        log_list = invest_log_service.search_by_user_id(state["user_id"])

        if(action == "매수"):
            won_asset = next((asset for asset in assets if asset.stock_code == "0"), None)
            won_total = won_asset.amount if won_asset else 0
            amount_ratio = 0 if won_total==0 else amount / won_total
            invest_log_service.create(
                state["user_id"], 
                date, 
                dart_corp_code.corp_code, 
                stock_name, 
                action, 
                amount, 
                reason,
                amount_ratio,
                0,
                0,
                price,
            )
        else:
            stock_asset = next((asset for asset in assets if asset.stock_code == dart_corp_code.corp_code), None)
            stock_total = stock_asset.amount if stock_asset else 0
            amount_ratio = 0 if stock_total==0 else amount / stock_total
            # 매수평균가 계산
            buy_logs = [log for log in log_list if log.stock_code == dart_corp_code.corp_code and log.action == "매수"]
            
            if len(buy_logs) == 0:
                average_price = 0
            else:
                total_cost = sum(log.price * log.amount for log in buy_logs)
                total_amount = sum(log.amount for log in buy_logs)
                average_price = total_cost / total_amount if total_amount > 0 else 0

            profit = (price - average_price) * amount
            profit_ratio = 0 if average_price==0 else profit / (average_price * amount)
            
            invest_log_service.create(
                state["user_id"], 
                date, 
                dart_corp_code.corp_code, 
                stock_name, 
                action, 
                amount, 
                reason, 
                amount_ratio,
                profit,
                profit_ratio,
                price,
            )

        tool_message = ToolMessage(
            name="create_invest_log",
            content=f"매매일지 생성이 완료되었습니다.",
            tool_call_id=str(uuid.uuid4()),
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
        return {"action": "read"}

update_log_system_prompt = f"""
    오늘의 날짜: {datetime.now().strftime("%Y-%m-%d")}
    당신은 매매일지를 수정하는 agent입니다. 사용자의 매매일지를 수정해주세요.
    매매일지를 수정하기 위해서는 먼저 수정할 매매일지를 식별해야 합니다.
    수정할 매매일지 식별 정보:
    invest_log_id: str # 매매일지 ID (있는 경우)
    date: str # 매매일 (ID가 없는 경우 날짜로 식별)
    stock_name: str # 종목명 (ID가 없는 경우 종목명으로 식별)
    
    그 후 수정할 정보를 추출해주세요:
    update_date: str # 수정할 매매일 (변경하지 않으면 빈 값)
    update_stock_name: str # 수정할 종목명 (변경하지 않으면 빈 값)
    update_action: str # 수정할 매매 행동 (변경하지 않으면 빈 값)
    update_amount: int # 수정할 매매 수량 (변경하지 않으면 0)
    update_reason: str # 수정할 매매 이유 (변경하지 않으면 빈 값)
    update_price: int # 수정할 매매 가격 (변경하지 않으면 0)
"""

update_log_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", update_log_system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "위 대화를 참고하여 수정할 매매일지를 식별하고 수정할 정보를 정리해 주세요."
        ),
    ]
)

def invest_update_node(state: GraphState):
    formatted_prompt = update_log_prompt.format(messages=state["messages"])
    
    url = f"https://clovastudio.stream.ntruss.com/v3/chat-completions/HCX-007"
    
    headers = {
        "Authorization": f"Bearer {settings.CLOVASTUDIO_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "messages": [{"role": "user", "content": formatted_prompt}],
        "maxCompletionTokens": 200,
        "temperature": 0.1,
        "thinking": {
          "effort": "none",
        },
        "responseFormat": {
            "type": "json",
            "schema":{
                "type": "object",
                "properties": {
                    "invest_log_id": {
                        "type": "string",
                        "description": "매매일지 ID"
                    },
                    "date": {
                        "type": "string",
                        "description": "식별용 매매일"
                    },
                    "stock_name": {
                        "type": "string",
                        "description": "식별용 종목명"
                    },
                    "update_date": {
                        "type": "string",
                        "description": "수정할 매매일"
                    },
                    "update_stock_name": {
                        "type": "string",
                        "description": "수정할 종목명"
                    },
                    "update_action": {
                        "type": "string",
                        "enum": ["매수", "매도", ""]
                    },
                    "update_amount": {
                        "type": "number",
                        "description": "수정할 매매 수량"
                    },
                    "update_reason": {
                        "type": "string",
                        "description": "수정할 매매 이유"
                    },
                    "update_price": {
                        "type": "number",
                        "description": "수정할 매매 가격"
                    }
                }
            }
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_data = response.json()
        content = result_data["result"]["message"]["content"]
        
        parsed_content = json.loads(content)
        invest_log_id = parsed_content.get("invest_log_id", "")
        date = parsed_content.get("date", "")
        stock_name = parsed_content.get("stock_name", "")
        
        invest_log_repo = InvestLogRepository()
        invest_log_service = InvestLogService(invest_log_repo=invest_log_repo)
        
        # 수정할 매매일지 찾기
        existing_log = None
        
        if invest_log_id:
            try:
                existing_log = invest_log_service.find_by_id(invest_log_id)
            except:
                pass
        
        if not existing_log:
            # ID로 찾을 수 없으면 날짜와 종목명으로 찾기
            all_logs = invest_log_service.search_by_user_id(state["user_id"])
            for log in all_logs:
                if (date and log.date == date) and (stock_name and log.stock_name == stock_name):
                    existing_log = log
                    break
        
        if not existing_log:
            tool_message = ToolMessage(
                name="update_invest_log",
                content=f"수정할 매매일지를 찾을 수 없습니다. 매매일지 ID, 날짜, 종목명을 확인해주세요.\n다음행동: answer_agent를 통해 유저에게 추가 정보를 물어보기",
                tool_call_id=str(uuid.uuid4()),
            )
            return {
                "messages": state["messages"] + [tool_message]
            }
        
        # 수정할 정보 추출
        update_date = parsed_content.get("update_date", "")
        update_stock_name = parsed_content.get("update_stock_name", "")
        update_action = parsed_content.get("update_action", "")
        update_amount = parsed_content.get("update_amount", 0)
        update_reason = parsed_content.get("update_reason", "")
        update_price = parsed_content.get("update_price", 0)
        
        # 기존 값으로 업데이트 객체 생성
        updated_log = InvestLog(
            id=existing_log.id,
            user_id=existing_log.user_id,
            date=update_date if update_date else existing_log.date,
            stock_code=existing_log.stock_code,
            stock_name=update_stock_name if update_stock_name else existing_log.stock_name,
            action=update_action if update_action else existing_log.action,
            price=update_price if update_price > 0 else existing_log.price,
            amount=update_amount if update_amount > 0 else existing_log.amount,
            reason=update_reason if update_reason else existing_log.reason,
            amount_ratio=existing_log.amount_ratio,  # 이는 다시 계산해야 할 수도 있음
            profit=existing_log.profit,  # 이는 다시 계산해야 할 수도 있음
            profit_ratio=existing_log.profit_ratio,  # 이는 다시 계산해야 할 수도 있음
            created_at=existing_log.created_at
        )
        
        # 종목명이 변경된 경우 corp_code도 업데이트
        if update_stock_name and update_stock_name != existing_log.stock_name:
            corp_code_repo = DartCorpCodeRepository()
            dart_corp_code_service = DartCorpCodeService(corp_code_repo=corp_code_repo)
            dart_corp_code = dart_corp_code_service.find_by_corp_name(update_stock_name)
            if dart_corp_code is None:
                tool_message = ToolMessage(
                    name="update_invest_log",
                    content=f"종목명을 찾을 수 없습니다: {update_stock_name}\n다음행동: answer_agent를 통해 유저에게 추가 정보를 물어보기",
                    tool_call_id=str(uuid.uuid4()),
                )
                return {
                    "messages": state["messages"] + [tool_message]
                }
            updated_log.stock_code = dart_corp_code.corp_code
        
        invest_log_service.update(updated_log)
        
        tool_message = ToolMessage(
            name="update_invest_log",
            content=f"매매일지 수정이 완료되었습니다.",
            tool_call_id=str(uuid.uuid4()),
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
        
        # 오류 시 메시지 반환
        tool_message = ToolMessage(
            name="update_invest_log",
            content=f"매매일지 수정 중 오류가 발생했습니다.",
            tool_call_id=str(uuid.uuid4()),
        )
        return {
            "messages": state["messages"] + [tool_message]
        }

delete_log_system_prompt = f"""
    당신은 매매일지를 삭제하는 agent입니다. 사용자의 매매일지를 삭제해주세요.
    매매일지를 삭제하기 위해서는 삭제할 매매일지를 식별해야 합니다.
    삭제할 매매일지 식별 정보:
    invest_log_id: str # 매매일지 ID (있는 경우)
    date: str # 매매일 (ID가 없는 경우 날짜로 식별)
    stock_name: str # 종목명 (ID가 없는 경우 종목명으로 식별)
"""

delete_log_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", delete_log_system_prompt),
        MessagesPlaceholder(variable_name="messages"),
        (
            "assistant",
            "위 대화를 참고하여 삭제할 매매일지를 식별해 주세요."
        ),
    ]
)

def invest_delete_node(state: GraphState):
    formatted_prompt = delete_log_prompt.format(messages=state["messages"])
    
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
                    "invest_log_id": {
                        "type": "string",
                        "description": "매매일지 ID"
                    },
                    "date": {
                        "type": "string",
                        "description": "식별용 매매일"
                    },
                    "stock_name": {
                        "type": "string",
                        "description": "식별용 종목명"
                    }
                }
            }
        }
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        result_data = response.json()
        content = result_data["result"]["message"]["content"]
        
        parsed_content = json.loads(content)
        invest_log_id = parsed_content.get("invest_log_id", "")
        date = parsed_content.get("date", "")
        stock_name = parsed_content.get("stock_name", "")
        
        invest_log_repo = InvestLogRepository()
        invest_log_service = InvestLogService(invest_log_repo=invest_log_repo)
        
        # 삭제할 매매일지 찾기
        existing_log = None
        
        if invest_log_id:
            try:
                existing_log = invest_log_service.find_by_id(invest_log_id)
            except:
                pass
        
        if not existing_log:
            # ID로 찾을 수 없으면 날짜와 종목명으로 찾기
            all_logs = invest_log_service.search_by_user_id(state["user_id"])
            for log in all_logs:
                if (date and log.date == date) and (stock_name and log.stock_name == stock_name):
                    existing_log = log
                    break
        
        if not existing_log:
            tool_message = ToolMessage(
                name="delete_invest_log",
                content=f"삭제할 매매일지를 찾을 수 없습니다. 매매일지 ID, 날짜, 종목명을 확인해주세요.\n다음행동: answer_agent를 통해 유저에게 추가 정보를 물어보기",
                tool_call_id=str(uuid.uuid4()),
            )
            return {
                "messages": state["messages"] + [tool_message]
            }
        
        # 매매일지 삭제
        invest_log_service.delete(existing_log.id)
        
        tool_message = ToolMessage(
            name="delete_invest_log",
            content=f"매매일지가 성공적으로 삭제되었습니다. (삭제된 일지: {existing_log.date} - {existing_log.stock_name})",
            tool_call_id=str(uuid.uuid4()),
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
        
        # 오류 시 메시지 반환
        tool_message = ToolMessage(
            name="delete_invest_log",
            content=f"매매일지 삭제 중 오류가 발생했습니다.",
            tool_call_id=str(uuid.uuid4()),
        )
        return {
            "messages": state["messages"] + [tool_message]
        }