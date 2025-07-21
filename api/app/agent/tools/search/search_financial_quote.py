from langchain_core.tools import tool
from app.crawl.application.quote_service import search_quote
from langgraph.types import Command
from langgraph.graph import MessagesState
from langgraph.prebuilt import InjectedState
from typing import Annotated
from langchain_core.tools import tool, InjectedToolCallId

@tool
async def search_financial_quote(companyName: str, state: Annotated[MessagesState, InjectedState], tool_call_id: Annotated[str, InjectedToolCallId]):
    """
    companyName(기업의 이름을 기준으로) 주식 시장 관련 정보를 검색합니다.
    이 tool을 이용하여 얻을 수 있는 세부 정보는
    1. 기업명(name)
    2. 현재 주가(price)
    3. 상장 거래소(exchange)
    4. 티커(symbol)
    5. 통화(currency)
    6. 전일 종가(prevDayClosePrice)
    7. 시가총액(marketCapitalization)
    8. 기업 정보(information)
    """
    result = await search_quote(companyName)
    crawled = result["crawled"]
    context = f"""<finalcial_quote>{crawled}</finalcial_quote>"""
    tool_message = {
        "role": "tool",
        "content": context,
        "name": "search_financial_quote",
        "tool_call_id": tool_call_id,
    }
    return Command(update={"messages":state["messages"] + [tool_message]})