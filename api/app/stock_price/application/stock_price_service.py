from app.config import get_settings
import requests
from app.dart.application.corp_code_service import DartCorpCodeService
from app.stock_price.domain.stock_price import StockPrice, StockPriceItem
from fastapi import HTTPException
from app.crawl.application.quote_service import search_quote

settings = get_settings()


class StockPriceService:
    def __init__(
        self,
        corp_code_service: DartCorpCodeService,
    ):
        self.corp_code_service = corp_code_service

    async def get_by_corp_name(self, corp_name: str):
        corp_code = self.corp_code_service.find_by_corp_name(corp_name)
        likeSrtnCd = corp_code.stock_code
        
        base_url = "http://apis.data.go.kr/1160100/service/GetStockSecuritiesInfoService/getStockPriceInfo"
        params = {
            "serviceKey": settings.DATA_GO_API_KEY,
            "likeSrtnCd": likeSrtnCd,
            "resultType": "json",
            "numOfRows": 100,
            "pageNo": 1
        }
        
        res = requests.get(base_url, params=params);
        response = res.json()
        items = response["response"]["body"]["items"]["item"]

        if(len(items) == 0):
            raise HTTPException(status_code=404, detail="Stock price not found")

        quote = await search_quote(items[0]["srtnCd"])
        crawled = quote["crawled"][0]

        current_price = crawled["price"].replace(",", "")
        current_price = current_price.replace("₩", "")
        current_price = current_price.split(".")[0]
        current_price = int(current_price)

        prev_close = crawled["prevDayClosePrice"].replace(",", "")
        prev_close = prev_close.replace("₩", "")
        prev_close = prev_close.split(".")[0]
        prev_close = int(prev_close)

        result = StockPrice(
            stock_name=items[0]["itmsNm"],
            stock_code=items[0]["srtnCd"],
            current_price=current_price,
            change_price=current_price - prev_close,
            change_rate=((current_price - prev_close) / prev_close) * 100,
            unit="KRW",
            items=[StockPriceItem(
                    date=item["basDt"],
                    open=item["mkp"],
                    high=item["hipr"],
                    low=item["lopr"],
                    close=item["clpr"],
                    change=item["vs"],
                    change_rate=item["fltRt"]
                ) for item in items]
            )

        return result

        