from app.config import get_settings
import requests
from app.dart.application.corp_code_service import DartCorpCodeService
from app.stock_price.domain.stock_price import StockPrice, StockPriceItem
from fastapi import HTTPException

settings = get_settings()


class StockPriceService:
    def __init__(
        self,
        corp_code_service: DartCorpCodeService,
    ):
        self.corp_code_service = corp_code_service    

    def get_by_corp_name(self, corp_name: str):
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

        result = StockPrice(
            stock_name=items[0]["itmsNm"],
            stock_code=items[0]["srtnCd"],
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

        