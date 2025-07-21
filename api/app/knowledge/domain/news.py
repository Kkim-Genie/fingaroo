from datetime import datetime
from pydantic import BaseModel

class News(BaseModel):
    id: str
    title: str
    link: str
    date: str
    content: str
    company: str
    created_at: datetime
    updated_at: datetime
    keywords: list[str]

class CreateNewsBodyElem(BaseModel):
    title: str
    content: str
    company: str
    keywords: str
    link: str
    date: str

class CreateNewsBody(BaseModel):
    news: list[CreateNewsBodyElem]