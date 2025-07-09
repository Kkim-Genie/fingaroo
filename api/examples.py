import asyncio
import os
import json
import base64
from pathlib import Path
from typing import List
from crawl4ai import ProxyConfig

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode, CrawlResult
from crawl4ai import RoundRobinProxyStrategy
from crawl4ai import JsonCssExtractionStrategy, LLMExtractionStrategy
from crawl4ai import LLMConfig
from crawl4ai import PruningContentFilter, BM25ContentFilter
from crawl4ai import DefaultMarkdownGenerator
from crawl4ai import BFSDeepCrawlStrategy, DomainFilter, FilterChain
from crawl4ai import BrowserConfig

# Define current directory
__cur_dir__ = os.path.dirname(os.path.abspath(__file__))

def save_markdown(markdown: str, filename: str):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(markdown)
    print(f"Saved markdown to {filename}")

async def demo_basic_crawl():
    """Basic web crawling with markdown generation"""
    print("\n=== 1. Basic Web Crawling ===")
    async with AsyncWebCrawler(config = BrowserConfig(
        viewport_height=800,
        viewport_width=1200,
        headless=True,
        verbose=True,
    )) as crawler:
        results: List[CrawlResult] = await crawler.arun(
            url="https://www.google.com/finance/quote/META:NASDAQ?hl=ko"
        )

        for i, result in enumerate(results):
            print(f"Result {i + 1}:")
            print(f"Success: {result.success}")
            if result.success:
                print(f"Markdown length: {len(result.markdown.raw_markdown)} chars")
                print(f"First 100 chars: {result.markdown.raw_markdown[:100]}...")
                save_markdown(result.markdown.raw_markdown, f"result.md")
            else:
                print("Failed to crawl the URL")

async def demo_fit_markdown():
    """Generate focused markdown with LLM content filter"""
    print("\n=== 3. Fit Markdown with LLM Content Filter ===")

    async with AsyncWebCrawler() as crawler:
        result: CrawlResult = await crawler.arun(
            url="https://www.google.com/finance/quote/META:NASDAQ?hl=ko",
            config=CrawlerRunConfig(
                markdown_generator=DefaultMarkdownGenerator(
                    content_filter=PruningContentFilter()
                )
            ),
        )

        # Print stats and save the fit markdown
        print(f"Raw: {len(result.markdown.raw_markdown)} chars")
        print(f"Fit: {len(result.markdown.fit_markdown)} chars")
        save_markdown(result.markdown.raw_markdown, f"result.md")
        save_markdown(result.markdown.fit_markdown, f"result_fit.md")

async def demo_llm_structured_extraction_no_schema():
    # Create a simple LLM extraction strategy (no schema required)
    extraction_strategy = LLMExtractionStrategy(
        llm_config=LLMConfig(
            provider="openai/gpt-4o-mini",
            api_token="env:OPENAI_API_KEY",
        ),
        instruction="""
        google finance quote page, extract all the information about the stock.
        name language priority is korean then english
        marketCapitalization must be calculated based on marketCapitalizationCurrency

        """,
        extract_type="schema",
        schema="{name: string, exchange: string, symbol:string, currency:string, price:float, prevDayClosePrice:float, marketCapitalization:float, marketCapitalizationCurrency:string}",
        extra_args={
            "temperature": 0.0,
        },
    )

    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

    async with AsyncWebCrawler() as crawler:
        results: List[CrawlResult] = await crawler.arun(
            "https://www.google.com/finance/quote/005930:KRX?hl=ko", config=config, headers={"Accept-Language": "ko-KR,ko;q=0.9"}
        )

        for result in results:
            print(f"URL: {result.url}")
            print(f"Success: {result.success}")
            if result.success:
                data = json.loads(result.extracted_content)
                print(json.dumps(data, indent=2))
            else:
                print("Failed to extract structured data")

async def generate_finance_quote_schema():
    """Extract structured data using CSS selectors"""
    print("\n=== 5. CSS-Based Structured Extraction ===")
    # Sample HTML for schema generation (one-time cost)
    with open("app/core/page_examples/google_finance_example.html", "r", encoding="utf-8") as f:
        sample_html = f.read()
    schema = JsonCssExtractionStrategy.generate_schema(
        html=sample_html,
        llm_config=LLMConfig(
            provider="openai/gpt-4.1",
            api_token="env:OPENAI_API_KEY",
        ),
        query="""
        google finance quote page, extract all the information about the stock.
        name language priority is korean then english
        marketCapitalization must be include all part of unit and exchange
        Please generate a schema for this finance quote page
        ###structure of schema
        {
            name: string (예: 삼성전자),
            price: string,
            exchange: string (예: KRX),
            symbol:string,
            currency:string (예: KRW, ₩, USD, $),
            prevDayClosePrice:string, 
            marketCapitalization:string, 
            information:string,
        }
        """,
    )
        
    # Save schema to schemas/finance_quote.json
    os.makedirs("app/core/crawl_schemas", exist_ok=True)
    with open("app/core/crawl_schemas/finance_quote.json", "w", encoding="utf-8") as f:
        json.dump(schema, f, ensure_ascii=False, indent=2)
    print("Schema saved to schemas/finance_quote.json")

async def demo_css_structured_extraction_no_schema():
    """Extract structured data using CSS selectors"""
    print("\n=== 5. CSS-Based Structured Extraction ===")
    schema_file_path = f"{__cur_dir__}/schemas/finance_quote.json"
    if os.path.exists(schema_file_path):
        with open(schema_file_path, "r") as f:
            schema = json.load(f)
    else:
        raise FileNotFoundError(f"Schema file not found at {schema_file_path}. Please run generate_finance_quote_schema() first.")

    # Create no-LLM extraction strategy with the generated schema
    extraction_strategy = JsonCssExtractionStrategy(schema)
    config = CrawlerRunConfig(extraction_strategy=extraction_strategy)

    # Use the fast CSS extraction (no LLM calls during extraction)
    async with AsyncWebCrawler() as crawler:
        result:CrawlResult = await crawler.arun(
            "https://www.google.com/finance/quote/005930:KRX?hl=ko", config=config
        )

        if result.success:
            print(result.extracted_content)
        else:
            print("Failed to extract structured data")

async def demo_js_interaction():
    """Execute JavaScript to load more content"""
    print("\n=== 7. JavaScript Interaction ===")

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

    schema_file_path = f"{__cur_dir__}/schemas/finance_quote.json"
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

            searchText = "삼성전자";
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

        for result in result2:
            print(f"URL: {result.url}")
            print(f"Success: {result.success}")
            if result.success:
                data = json.loads(result.extracted_content)
                print(data)
            else:
                print("Failed to extract structured data")

        await crawler.crawler_strategy.kill_session(session_id)


async def main():
    # await demo_basic_crawl()
    # await demo_fit_markdown()
    # await demo_llm_structured_extraction_no_schema()
    await generate_finance_quote_schema()
    # await demo_css_structured_extraction_no_schema()
    # await demo_js_interaction()

if __name__ == "__main__":
    asyncio.run(main())
