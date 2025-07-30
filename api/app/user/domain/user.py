from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: str
    name: str
    email: str
    gender: str
    birthyear: int
    reg_date: datetime