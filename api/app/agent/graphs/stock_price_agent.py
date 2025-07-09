from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from app.config import get_settings
from app.agent.tools.stock_price.search_indicator_id_tool import search_indicator_id_tool
from app.agent.tools.stock_price.search_stock_price_tool import search_stock_price_tool

settings = get_settings()

tools = [search_indicator_id_tool, search_stock_price_tool]

def stock_price_agent():
    llm = ChatGoogleGenerativeAI(model=settings.LLM_MODEL, api_key=settings.GOOGLE_API_KEY)

    stock_price_agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt="""
        당신은 여러 기업/ETF의 주가 데이터를 검색하는 assistant입니다. 당신에게 주어진 tool을 반드시 사용하여 검색을 수행합니다.

        여러 기업/ETF의 주가 데이터를 검색합니다. 세부 검색 기능들은 아래와 같습니다.
            1. 지표의 id 및 기본정보 검색
            2. 지표의 id를 기반하여 주가 데이터 검색

        추가 지시 사항
        1. 주가의 지표 id는 서비스에서 따로 관리하는 id입니다. 기업명만 알고 있다면 기본정보 검색 Tool을 이용하여 먼저 검색을 수행하여야 합니다.
        2. 사용자에 질문에 대해 직접적으로 답하지말고 이에 필요한 내용만 검색하세요. 직접적인 답변은 당신의 검색결과를 통해 다른 assistant가 수행할 겁니다. 당신의 역할에만 충실하세요.
        3. 기간에 대한 특별한 언급이 없다면 1주일 전부토 오늘까지의 주가를 검색하세요
        4. dataAggregation은 기본값으로 eop을 사용하세요
        """,
        name="stock_price_agent"
    )
    return stock_price_agent
