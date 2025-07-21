from app.agent.tools.search.naver_search import naver_search
from app.agent.tools.search.search_financial_quote import search_financial_quote
from app.agent.tools.search.search_news import search_news
from app.agent.tools.search.search_daily_report import search_daily_report
from app.agent.tools.search.search_knowledge_base import search_knowledge_base
from langgraph.prebuilt import create_react_agent
from app.config import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime
from langgraph.checkpoint.memory import InMemorySaver

settings = get_settings()

tools = [naver_search, search_financial_quote, search_news, search_daily_report, search_knowledge_base]

def search_agent():
    today_date = datetime.now().strftime("%Y-%m-%d")
    llm = ChatGoogleGenerativeAI(model=settings.LLM_MODEL, api_key=settings.GOOGLE_API_KEY)
    checkpointer = InMemorySaver()
    search_agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=f"""
        당신은 경제 관련 데이터를 검색하는 assistant입니다. 당신에게 주어진 tool을 반드시 사용하여 검색을 수행합니다.
        오늘의 날짜는 {today_date}입니다. 이 날짜를 기준으로 검색을 수행합니다.

        경제 관련된 다양한 정보를 검색합니다. 답변을 하기 위한 충분한 정보가 있을 경우 실행하지 않습니다. 세부 검색 기능들은 아래와 같습니다.
            1. 네이버 뉴스 검색
            2. google finance에서 기본 기업 정보 검색
            3. 경제 관련 뉴스 검색(날짜를 기준으로 검색)
            4. 일간 시황 검색(날짜를 기준으로 검색)
            5. 경제 관련 지식 베이스 검색 

        추가 지시 사항
        1. 경제와 관련없는 내용이라면 절대 사용하지 않습니다.
        2. 검색 결과가 없다면 검색 결과가 없다고 알려주세요.
        3. 검색 결과가 있다면 검색 결과를 알려주세요.
        4. 사용자에 질문에 대해 직접적으로 답하지말고 이에 필요한 내용만 검색하세요. 직접적인 답변은 당신의 검색결과를 통해 다른 assistant가 수행할 겁니다. 당신의 역할에만 충실하세요.
        5. 네이버 뉴스 검색은 경제 관련 뉴스 검색을 통해 필요한 내용을 찾지 못했을 경우 사용합니다.
        6. 사용자가 일반적인 뉴스를 물어본다면 경제 관련 뉴스를 검색합니다.
        7. 경제 관련 지식 베이스는 뉴스와 일간 보고서를 바탕으로 방대한 내용을 가지고 있습니다. 경제나 시대 흐름에 대한 내용을 찾아야 할 경우 최우선적으로 경제 관련 지식 베이스에서 검색을 수행합니다.
        """,
        name="search_agent",
        checkpointer=checkpointer
    )
    return search_agent
