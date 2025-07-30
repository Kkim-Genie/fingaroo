from datetime import datetime
from pydantic import BaseModel

class News(BaseModel):
    id: str
    title: str
    link: str
    date: str
    content: str
    type: str
    created_at: datetime
    updated_at: datetime

class CreateNewsBodyElem(BaseModel):
    title: str
    content: str
    type: str
    link: str
    date: str

class CreateNewsBody(BaseModel):
    news: list[CreateNewsBodyElem]