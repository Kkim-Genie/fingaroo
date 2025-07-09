from langchain_core.tools import tool
from app.config import get_settings
import requests

settings = get_settings()

tool_description = f"""
특정 기업의 주가를 검색하기 위한 고유 Id및 기본 정보를 검색하는 tool입니다. symbol을 기준으로 검색하고 가장 유사도 높은 3개를 순서대로 반환합니다.

### tool input
symbol: str,  # 조회할 기업/ETF 심볼

#tool output
id: 고유 id,
index: 지표 인덱스,
indicatorType: 지표 타입,
symbol: 기업/ETF 심볼,
name: 기업/ETF 이름,
unit: 지표 단위,
country: 국가,
currency: 통화,
exchange: 거래소,
micCode: 거래소 코드,
figiCode: 국제 거래소 코드,
type: 지표 타입
"""

@tool(description=tool_description)
def search_indicator_id_tool(symbol: str) -> str:
    API_URL = f"{settings.API_URL}/api/numerical-guidance/indicator/search?keyword={symbol}"
    response = requests.get(API_URL)
    result = response.json()
    if(len(result) > 3):
        result = result[:3]

    result_str = f"<indicator_search_result>{result}</indicator_search_result>"

    return result_str