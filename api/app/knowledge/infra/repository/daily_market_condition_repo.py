from fastapi import HTTPException

from app.database import SessionLocal
from app.knowledge.domain.repository.daily_market_condition_repo import IDailyMarketConditionRepository
from app.knowledge.infra.db_models.daily_market_condition import DailyMarketCondition
from app.utils.db_utils import row_to_dict
from app.utils.knowledge_utils import make_weekly_report_dates


class DailyMarketConditionRepository(IDailyMarketConditionRepository):
    def get_first(self) -> DailyMarketCondition:
        with SessionLocal() as db:
            daily_market_condition = db.query(DailyMarketCondition).first()

        if not daily_market_condition:
            raise HTTPException(status_code=422)

        return DailyMarketCondition(**row_to_dict(daily_market_condition))

    def search_by_id(self, id: str) -> list[DailyMarketCondition]:
        with SessionLocal() as db:
            daily_market_condition = db.query(DailyMarketCondition).filter(DailyMarketCondition.id == id).all()

        if not daily_market_condition:
            raise HTTPException(status_code=422)

        return [DailyMarketCondition(**row_to_dict(daily_market_condition)) for daily_market_condition in daily_market_condition]

    def find_by_date(self, date: str) -> list[DailyMarketCondition]:
        with SessionLocal() as db:
            daily_market_condition = db.query(DailyMarketCondition).filter(DailyMarketCondition.date == date).all()

        if not daily_market_condition:
            raise HTTPException(status_code=422)

        return [DailyMarketCondition(**row_to_dict(daily_market_condition)) for daily_market_condition in daily_market_condition]

    def create(self, daily_market_condition: DailyMarketCondition):
        with SessionLocal() as db:
            db.add(daily_market_condition)
            db.commit()

    def get_weekly_report_contexts(self, end_date:str) -> tuple[str, list[str]]:
        datesToFetch = make_weekly_report_dates(end_date)

        with SessionLocal() as db:
            rows = db.query(DailyMarketCondition).filter(DailyMarketCondition.date.in_(datesToFetch)).all()

        data = [row_to_dict(row) for row in rows]

        market_analysis_ids = [row["id"] for row in data]

        contexts = ""
        for row in data:
            contexts += f"<document><date>{row['date']}</date><content>{row['content']}</content></document>"

        return contexts, market_analysis_ids