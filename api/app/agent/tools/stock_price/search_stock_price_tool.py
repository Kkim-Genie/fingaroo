from langchain_core.tools import tool
from app.config import get_settings
import requests

settings = get_settings()

tool_description = f"""
id를 기반하여 특정 기업의 주가를 검색하는 tool입니다. 
- 한번에 30개 이상의 데이터를 조회할 수 없습니다.
- 많은 양의 데이터를 조회하는 것이 비용이 높습니다. 꼭 필요한 기간에 대해서만 검색하세요.

### tool input
indicatorId: str,  # 조회할 지표 id
interval: str,  # 조회할 주기(day, week, week2, month, quarter, half, year)
dataAggregation: str,  # 데이터 집계 방식(eop, sum, avg) (기본값: eop)
indicatorType: str,  # 지표 타입(stock, forex_pair, cryptocurrency, bond, fund, etf, commodity, economy)
startDate: str,  # 조회 시작일(YYYY-MM-DD)
endDate: str  # 조회 종료일(YYYY-MM-DD)

#tool output
indicator: 해당 지표의 기본 정보
values: 날짜별 주가 데이터
"""

@tool(description=tool_description)
def search_stock_price_tool(indicatorId: str, interval: str, dataAggregation: str, indicatorType: str, startDate: str, endDate: str) -> str:
    API_URL = f"{settings.API_URL}/api/numerical-guidance/indicators/live"
    params = {
        "indicatorId": indicatorId,
        "interval": interval,
        "dataAggregation": dataAggregation,
        "indicatorType": indicatorType,
        "startDate": startDate,
        "endDate": endDate
    }
    response = requests.get(API_URL, params=params)
    values = response.json()["values"]
    if(len(values) > 30):
        return "한번에 30개 이상의 데이터를 조회할 수 없습니다."

    result_str = f"<stock_price_result>{values}</stock_price_result>"

    return result_str