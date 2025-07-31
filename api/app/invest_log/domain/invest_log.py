from datetime import datetime
from pydantic import BaseModel

class InvestLog(BaseModel):
    id: str
    user_id: str
    date: str
    stock_code: str
    stock_name: str
    action: str
    price: int
    amount: int
    reason: str
    amount_ratio: float
    profit: int
    profit_ratio: float
    created_at: datetime

class CreateInvestLogBody(BaseModel):
    access_token: str
    refresh_token: str
    date: str
    stock_code: str
    stock_name: str
    action: str
    price: int
    amount: int
    reason: str
    amount_ratio: float
    profit: int
    profit_ratio: float

class UpdateInvestLogBody(BaseModel):
    access_token: str
    refresh_token: str
    invest_log: InvestLog

class DeleteInvestLogBody(BaseModel):
    access_token: str
    refresh_token: str
    invest_log_id: str