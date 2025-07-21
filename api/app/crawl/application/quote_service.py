import os
import json
from typing import List

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, CrawlResult
from crawl4ai import JsonCssExtractionStrategy
from crawl4ai import BrowserConfig

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

    schema_file_path = f"../../utils/crawl_schemas/finance_quote.json"
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
