from app.agent.tools.naver_search import naver_search
from app.agent.tools.search_financial_quote import search_financial_quote
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import get_settings

settings = get_settings()

tools = [naver_search, search_financial_quote]

def search_agent():
    llm = ChatGoogleGenerativeAI(model=settings.LLM_MODEL, api_key=settings.GOOGLE_API_KEY)

    search_agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt="""
        당신은 경제 관련 데이터를 검색하는 assistant입니다. 당신에게 주어진 tool을 반드시 사용하여 검색을 수행합니다.

        경제 관련된 다양한 정보를 검색합니다. 답변을 하기 위한 충분한 정보가 있을 경우 실행하지 않습니다. 세부 검색 기능들은 아래와 같습니다.
            1. 네이버 뉴스 검색
            2. google finance에서 기본 기업 정보 검색

        추가 지시 사항
        1. 경제와 관련없는 내용이라면 절대 사용하지 않습니다.
        2. 검색 결과가 없다면 검색 결과가 없다고 알려주세요.
        3. 검색 결과가 있다면 검색 결과를 알려주세요.
        4. 사용자에 질문에 대해 직접적으로 답하지말고 이에 필요한 내용만 검색하세요. 직접적인 답변은 당신의 검색결과를 통해 다른 assistant가 수행할 겁니다. 당신의 역할에만 충실하세요.
        """,
        name="search_agent"
    )
    return search_agent
