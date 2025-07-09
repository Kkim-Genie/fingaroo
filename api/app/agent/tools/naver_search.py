from langchain_core.tools import tool
from app.config import get_settings
import requests

settings = get_settings()

@tool
def naver_search(query: str) -> str:
    """
    네이버 뉴스 검색 결과를 반환합니다.
    """
    url = settings.NAVER_SEARCH_URL
    headers = {
        "X-Naver-Client-Id": settings.NAVER_CLIENT_ID,
        "X-Naver-Client-Secret": settings.NAVER_CLIENT_SECRET,
    }
    params = {
        "query": query,
        "display": 10,
    }
    response = requests.get(url, headers=headers, params=params)
    result = response.json()
    items = result.get("items", [])
    result_str = "\n".join([f"""<document>
    <title>{item['title']}</title>
    <link>{item['link']}</link>
    <description>{item['description']}</description>
    </document>\n""" for item in items])

    return result_str