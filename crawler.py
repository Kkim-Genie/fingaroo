import os
import json
from typing import List

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, CrawlResult
from crawl4ai import JsonCssExtractionStrategy
from crawl4ai import BrowserConfig
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig

import io
import asyncio
import requests

from pdfminer.high_level import extract_text

__root_dir__ = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))

async def search_quote(query: str):
    session_id = "google_finance_quote"
    base_wait = """js:() => {
        const inputElement = document.querySelectorAll('#yDmH0d > c-wiz.zQTmif.SSPGKf.ccEnac > div > div.KdK6Xc > div.e1AOyf > div > div > div > div.d1dlne > input.Ax4B8.ZAGvjd');
        return inputElement.length > 0;
    }"""

    config1 = CrawlerRunConfig(
        wait_for=base_wait,
        session_id=session_id,
        cache_mode=CacheMode.BYPASS,
        # Not using js_only yet since it's our first load
    )

    schema_file_path = f"{__root_dir__}/app/utils/crawl_schemas/finance_quote.json"
    if os.path.exists(schema_file_path):
        with open(schema_file_path, "r") as f:
            schema = json.load(f)
    else:
        raise FileNotFoundError(f"Schema file not found at {schema_file_path}. Please run generate_finance_quote_schema() first.")

    # Create no-LLM extraction strategy with the generated schema
    extraction_strategy = JsonCssExtractionStrategy(schema)

    # A simple page that needs JS to reveal content
    async with AsyncWebCrawler(config=BrowserConfig(headless=True)) as crawler:
        # Initial load
        result = await crawler.arun(
            url="https://www.google.com/finance/?hl=ko",
            config=config1,
        )

        js_next_page = """
            inputElement = document.querySelector('#yDmH0d > c-wiz.zQTmif.SSPGKf.ccEnac > div > div.KdK6Xc > div.e1AOyf > div > div > div > div.d1dlne > input.Ax4B8.ZAGvjd');

            searchText = "{}";
            """.format(query)+ """
            inputElement.value = searchText;
            for (let i = 0; i < searchText.length; i++) {
                const keydownEvent = new KeyboardEvent('keydown', { key: searchText[i], code: `Key${searchText[i].toUpperCase()}`, char: searchText[i], keyCode: searchText.charCodeAt(i), which: searchText.charCodeAt(i), bubbles: true });
                inputElement.dispatchEvent(keydownEvent);
            }
            inputElement.dispatchEvent(new Event('input', { bubbles: true }));
            inputElement.dispatchEvent(new Event('change', { bubbles: true }));
            const enterKeyEvent = new KeyboardEvent('keydown', {
                key: 'Enter',
                code: 'Enter',
                which: 13,
                keyCode: 13,
                bubbles: true,
                cancelable: true
            });
            inputElement.dispatchEvent(enterKeyEvent);
            """
        
        wait_for_next = """js:() => {
            const title = document.querySelectorAll('div.zzDege');
            return title.length > 0;
        }"""

        # Click "More" link
        config_next = CrawlerRunConfig(
            session_id=session_id,
            js_code=js_next_page,
            js_only=True,  # Continue in same page
            wait_for=wait_for_next,
            cache_mode=CacheMode.BYPASS,
            extraction_strategy=extraction_strategy
        )

        result2 = await crawler.arun(
            url="https://www.google.com/finance/?hl=ko", config=config_next
        )

        # Handle single result - type ignore due to crawl4ai type confusion
        if result2.success and result2.extracted_content:  # type: ignore
            crawled = json.loads(result2.extracted_content)  # type: ignore
        else:
            return {"crawled": [], "success": False, "reason": "Failed to extract structured data"}

        # Close the session
        try:
            await crawler.close()
        except:
            pass

        return {"crawled": crawled, "success": True}

# 브라우저 보안 우회용 설정
browser_config = BrowserConfig(
    headless=False,  # 실제 브라우저 창을 띄움
    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)

async def crawl_miraeasset_reports(page: int = 1):
    """
    미래에셋증권 리서치/크롤러 보고서 목록 페이지에서
    각 보고서의 제목, 날짜, PDF 다운로드 링크를 크롤링합니다.
    Args:
        page (int): 페이지 번호 (기본값 1)
    Returns:
        List[dict]: [{"title": str, "date": str, "pdf_url": str}]
    """
    from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, BrowserConfig

    base_url = f"https://securities.miraeasset.com/bbs/board/message/list.do?categoryId=1521&pageIndex={page}"
    session_id = f"miraeasset_reports_{page}"

    # 보고서 목록이 로드될 때까지 대기
    wait_for = """js:() => {
        const rows = document.querySelectorAll('table tbody tr');
        return rows.length > 0;
    }"""

    config = CrawlerRunConfig(
        wait_for=wait_for,
        session_id=session_id,
        cache_mode=CacheMode.BYPASS,
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=base_url,
            config=config,
        )
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(result.html, "html.parser")
        rows = soup.select("table tbody tr")
        reports = []
        for row in rows:
            # 제목
            title_tag = row.select_one("td:nth-child(2) a")
            title = title_tag.text.strip() if title_tag else None
            # 상세페이지 URL
            detail_url = None
            if title_tag and title_tag.has_attr('href'):
                href = title_tag['href']
                if isinstance(href, list):
                    href = href[0] if href else ''
                if isinstance(href, str) and href.startswith("javascript:view"):
                    # javascript:view('2333274','2494') 형태에서 게시글 id 추출
                    import re
                    m = re.search(r"view\\('([0-9]+)','([0-9]+)'", href)
                    if m:
                        post_id, category_id = m.group(1), m.group(2)
                        detail_url = f"https://securities.miraeasset.com/bbs/board/message/view.do?categoryId={category_id}&messageId={post_id}"
            # 날짜
            date_tag = row.select_one("td:nth-child(4)")
            date = date_tag.text.strip() if date_tag else None
            # PDF 다운로드 링크
            pdf_tag = row.select_one("td:nth-child(3) a")
            pdf_url = None
            if pdf_tag and pdf_tag.has_attr('href'):
                href = pdf_tag['href']
                if isinstance(href, list):
                    href = href[0] if href else ''
                if isinstance(href, str) and href.startswith("javascript:downConfirm"):
                    # 추출: javascript:downConfirm('pdf_url', ...)
                    import re
                    m = re.search(r"downConfirm\\('([^']+)'", href)
                    if m:
                        pdf_url = m.group(1)
            if title and date and pdf_url and detail_url:
                reports.append({
                    "title": title,
                    "date": date,
                    "pdf_url": pdf_url,
                    "detail_url": detail_url
                })
        try:
            await crawler.close()
        except:
            pass
        return reports

async def get_report_body(detail_url: str) -> str:
    """
    미래에셋증권 리서치 상세페이지에서 본문 텍스트를 추출합니다.
    Args:
        detail_url (str): 상세페이지 URL
    Returns:
        str: 본문 텍스트
    """

    wait_for = """js:() => {
        const content = document.querySelectorAll('.bbs_view_cont');
        return content.length > 0;
    }"""
    config = CrawlerRunConfig(
        wait_for=wait_for,
        session_id="miraeasset_detail",
        cache_mode=CacheMode.BYPASS,
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url=detail_url,
            config=config,
        )
        # 렌더링 대기 (1초)
        await asyncio.sleep(1)
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(result.html, "html.parser")
        content = soup.select_one('.bbs_view_cont')
        text = content.get_text(separator='\n', strip=True) if content else ''
        try:
            await crawler.close()
        except:
            pass
        return text

async def extract_pdf_text(pdf_url: str) -> str:
    """
    PDF 파일을 다운로드하고 텍스트를 추출합니다.
    Args:
        pdf_url (str): PDF 다운로드 URL
    Returns:
        str: PDF 내 텍스트
    """
    try:
        response = requests.get(pdf_url, timeout=20)
        response.raise_for_status()
        with io.BytesIO(response.content) as pdf_file:
            text = extract_text(pdf_file)
        return text.strip()
    except Exception as e:
        return f"[PDF 추출 실패: {e}]"

async def crawl_full_miraeasset_reports(page: int = 1):
    """
    미래에셋증권 보고서의 날짜, 제목, 본문, PDF 내 텍스트를 모두 포함하는 통합 크롤링 함수
    Returns:
        List[dict]: [{"date":..., "title":..., "body":..., "pdf_text":...}]
    """
    reports = await crawl_miraeasset_reports(page)
    results = []
    for report in reports:
        title = report.get("title")
        date = report.get("date")
        detail_url = report.get("detail_url")
        pdf_url = report.get("pdf_url")
        # 본문 추출
        body = await get_report_body(detail_url) if detail_url else ""
        # PDF 텍스트 추출
        pdf_text = await asyncio.to_thread(extract_pdf_text, pdf_url) if pdf_url else ""
        results.append({
            "date": date,
            "title": title,
            "body": body,
            "pdf_text": pdf_text
        })
    return results

test_detail_url = "https://securities.miraeasset.com/bbs/board/message/view.do?messageId=2333274&messageNumber=2494&messageCategoryId=0&startId=zzzzz%7E&startPage=1&curPage=1&searchType=2&searchText=&searchStartYear=2024&searchStartMonth=07&searchStartDay=17&searchEndYear=2025&searchEndMonth=07&searchEndDay=17&lastPageFlag=&vf_headerTitle=&categoryId=1521"
test_pdf_url = "https://securities.miraeasset.com/bbs/download/2137293.pdf?attachmentId=2137293"

async def main():
    # cralwer.py 내부 함수 import (파일명이 cralwer.py임에 주의!)
    from cralwer import get_report_body, extract_pdf_text

    # 상세페이지 본문 추출
    body = await get_report_body(test_detail_url)
    print("본문 텍스트:\n", body)
    print("="*80)

    # PDF 텍스트 추출
    pdf_text = await asyncio.to_thread(extract_pdf_text, test_pdf_url)
    print("PDF 텍스트:\n", pdf_text)

if __name__ == "__main__":
    asyncio.run(main())