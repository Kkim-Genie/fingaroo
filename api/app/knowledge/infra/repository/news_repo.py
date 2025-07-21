from fastapi import HTTPException
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.knowledge.domain.repository.news_repo import INewsRepository
from app.knowledge.infra.db_models.news import News
from app.utils.db_utils import row_to_dict
from app.utils.knowledge_utils import make_weekly_report_dates


class NewsRepository(INewsRepository):
    def get_first(self) -> News:
        with SessionLocal() as db:
            news = db.query(News).first()

        if not news:
            raise HTTPException(status_code=422)

        return News(**row_to_dict(news))

    def search_by_id(self, id: str) -> list[News]:
        with SessionLocal() as db:
            news = db.query(News).filter(News.id == id).all()

        return [News(**row_to_dict(news)) for news in news]

    def find_by_date(self, date: str) -> list[News]:
        with SessionLocal() as db:
            news = db.query(News).filter(News.date == date).all()

        return [News(**row_to_dict(news)) for news in news]

    def get_latest_news(self, type: str) -> News:
        with SessionLocal() as db:
            news = db.query(News).filter(News.company == type).order_by(News.date.desc()).first()

        return News(**row_to_dict(news))

    def create_news(self, news: list[News]):
        with SessionLocal() as db:
            db.add_all(news)
            db.commit()

    def get_daily_report_contexts(self, date:str) -> str:
        selected_date = datetime.strptime(date, '%Y-%m-%d').date()
        day = selected_date.weekday()
        datesToFetch = []

        if(day==1 or day==2 or day==3 or day==4):
            datesToFetch.append(selected_date.isoformat())
        else:
            diff_to_friday = (day - 4 + 7) % 7
            last_friday = selected_date - timedelta(days=diff_to_friday)

            current_date = last_friday
            while current_date <= selected_date:
                datesToFetch.append(current_date.isoformat()) # YYYY-MM-DD 형식
                current_date += timedelta(days=1) # 하루씩 증가

        with SessionLocal() as db:
            rows = db.query(News).filter(News.date.in_(datesToFetch)).all()

        data = [row_to_dict(row) for row in rows]

        contexts = ""
        for row in data:
            contexts += f"<document><title>{row['title']}</title><date>{row['date']}</date><content>{row['content']}</content></document>"

        return contexts

    def get_weekly_report_contexts(self, end_date:str) -> tuple[str, list[str]]:
        datesToFetch = make_weekly_report_dates(end_date)

        with SessionLocal() as db:
            rows = db.query(News).filter(News.date.in_(datesToFetch)).all()

        data = [row_to_dict(row) for row in rows]

        news_ids = [row["id"] for row in data]

        contexts = ""
        for row in data:
            contexts += f"<document><title>{row['title']}</title><date>{row['date']}</date><content>{row['content']}</content></document>"

        return contexts, news_ids