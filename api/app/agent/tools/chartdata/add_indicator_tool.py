from langchain_core.tools import tool
from app.config import get_settings
from langgraph.types import interrupt

settings = get_settings()

@tool
def add_indicator_tool(symbol: str) -> str:
    """
    차트데이터에 지표를 추가합니다.
    """
    human_response = interrupt(({"command": "add_indicator", "payload": {"symbol": symbol}}))
    result = human_response["result"]

    return result