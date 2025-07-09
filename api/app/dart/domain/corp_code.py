from pydantic import BaseModel
from datetime import datetime

class DartCorpCode(BaseModel):
    id: str
    corp_code: str
    corp_name: str
    corp_eng_name: str
    stock_code: str | None
    created_at: datetime
    updated_at: datetime