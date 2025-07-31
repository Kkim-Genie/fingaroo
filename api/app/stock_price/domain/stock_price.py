from datetime import datetime
from pydantic import BaseModel

class StockPriceItem(BaseModel):
    date: str
    open: int
    high: int
    low: int
    close: int
    change: int
    change_rate: float

class StockPrice(BaseModel):
    stock_name: str
    stock_code: str
    current_price: int
    change_price: int
    change_rate: float
    unit: str
    items: list[StockPriceItem]
    