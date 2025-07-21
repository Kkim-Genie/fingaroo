from pydantic import BaseModel
from datetime import datetime


class DailyMarketCondition(BaseModel):
    id:str
    date:str
    content:str
    created_at:datetime
    updated_at:datetime