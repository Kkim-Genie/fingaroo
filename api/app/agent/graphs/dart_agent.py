from app.agent.tools.dart.event.both_capital_decision_tool import both_capital_decision_tool
from app.agent.tools.dart.principal.changed_capital_tool import changed_capital_tool
from app.agent.tools.dart.event.company_divide_merge_tool import company_divide_merge_tool
from app.agent.tools.dart.event.company_divide_tool import company_divide_tool
from app.agent.tools.dart.event.company_merge_tool import company_merge_tool
from app.agent.tools.dart.event.convertible_bond_tool import convertible_bond_tool
from app.agent.tools.dart.event.free_capital_decision_tool import free_capital_decision_tool
from app.agent.tools.dart.event.law_suit_tool import law_suit_tool
from app.agent.tools.dart.principal.dividend_tool import dividend_tool
from app.agent.tools.dart.economy.financial_statement_tool import financial_statement_tool
from app.agent.tools.dart.economy.multi_company_account_tool import multi_company_account_tool
from app.agent.tools.dart.principal.multi_financial_indicator_tool import multi_financial_indicator_tool
from app.agent.tools.dart.event.paid_capital_decision_tool import paid_capital_decision_tool
from app.agent.tools.dart.economy.single_financial_indicator_tool import single_financial_indicator_tool
from app.agent.tools.dart.economy.single_company_account_tool import single_company_account_tool
from app.agent.tools.dart.event.stock_buyback_tool import stock_buyback_tool
from app.agent.tools.dart.event.stock_retirement_tool import stock_retirement_tool
from app.agent.tools.dart.principal.treasury_stock_tool import treasury_stock_tool
from app.agent.tools.dart.principal.total_stock_tool import total_stock_tool
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import get_settings

settings = get_settings()

tools = [
    both_capital_decision_tool, 
    changed_capital_tool, 
    company_divide_merge_tool, 
    company_divide_tool, 
    company_merge_tool, 
    convertible_bond_tool, 
    dividend_tool, 
    financial_statement_tool,
    free_capital_decision_tool,
    law_suit_tool,
    multi_company_account_tool,
    multi_financial_indicator_tool,
    paid_capital_decision_tool,
    single_financial_indicator_tool,
    single_company_account_tool,
    stock_buyback_tool,
    stock_retirement_tool,
    total_stock_tool,
    treasury_stock_tool
]

def dart_agent():
    llm = ChatGoogleGenerativeAI(model=settings.LLM_MODEL, api_key=settings.GOOGLE_API_KEY)

    dart_agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt="""
        당신은 dart api를 통해 한국 기업 관련 여러 재무 정보 및 이벤트 정보를 조회하는 assistant입니다. 당신에게 주어진 tool을 반드시 사용하여 검색을 수행합니다.

        경제 관련된 다양한 정보를 검색합니다. 답변을 하기 위한 충분한 정보가 있을 경우 실행하지 않습니다. 세부 검색 기능들은 아래와 같습니다.
            1. 특정 기업의 유상증자 및 무상증자 결정 정보 검색
            2. 특정 기업의 자본금 변동 정보 검색
            3. 특정 기업의 분할합병 정보 검색
            4. 특정 기업의 분할 정보 검색
            5. 특정 기업의 합병 정보 검색
            6. 특정 기업의 전환사채 정보 검색
            7. 특정 기업의 배당 정보 검색
            8. 특정 기업의 재무제표 정보 검색
            9. 특정 기업의 무상증자 결정 정보 검색
            10. 특정 기업의 소송 정보 검색
            11. 특정 기업의 다중회사 계정 정보 검색
            12. 특정 기업의 다중회사 재무지표 정보 검색
            13. 특정 기업의 유상증자 결정 정보 검색
            14. 특정 기업의 단일회사 재무지표 정보 검색
            15. 특정 기업의 단일회사 계정 정보 검색
            16. 특정 기업의 자사주매입 정보 검색
            17. 특정 기업의 자기주식 처분 결정 정보 검색
            18. 특정 기업의 주식총수 현황 정보 검색
            19. 특정 기업의 자기주식 현황 정보 검색
        추가 지시 사항
        1. 경제와 관련없는 내용이라면 절대 사용하지 않습니다.
        2. 검색 결과가 없다면 검색 결과가 없다고 알려주세요.
        3. 검색 결과가 있다면 검색 결과를 알려주세요.
        4. 사용자에 질문에 대해 직접적으로 답하지말고 이에 필요한 내용만 검색하세요. 직접적인 답변은 당신의 검색결과를 통해 다른 assistant가 수행할 겁니다. 당신의 역할에만 충실하세요.
        """,
        name="dart_agent"
    )
    return dart_agent
