from langgraph.prebuilt import create_react_agent
from app.config import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime
from app.agent.tools.chartdata.add_indicator_tool import add_indicator_tool
from langgraph.checkpoint.memory import InMemorySaver

settings = get_settings()

tools = [add_indicator_tool]

def chartdata_agent():
    checkpointer = InMemorySaver()
    today_date = datetime.now().strftime("%Y-%m-%d")
    llm = ChatGoogleGenerativeAI(model=settings.LLM_MODEL, api_key=settings.GOOGLE_API_KEY)

    chartdata_agent = create_react_agent(
        model=llm,
        tools=tools,
        prompt=f"""
        user는 여러 지표의 time series데이터를 담고 있는 차트데이터를 가지고 있습니다. 
        당신은 이 차트데이터를 관리하는 assistant입니다. 당신에게 주어진 tool을 반드시 사용하여 차트데이터를 관리합니다.
        오늘의 날짜는 {today_date}입니다. 이 날짜를 기준으로 차트데이터를 관리합니다.

        차트데이터를 관리합니다. 세부 검색 기능들은 아래와 같습니다.
            1. 차트데이터에 지표 추가

        추가 지시 사항
        """,
        name="chartdata_agent",
        checkpointer=checkpointer
    )
    return chartdata_agent
