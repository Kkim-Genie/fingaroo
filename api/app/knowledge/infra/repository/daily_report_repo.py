from fastapi import HTTPException

from app.database import SessionLocal
from app.knowledge.domain.repository.daily_report_repo import IDailyReportRepository
from app.knowledge.infra.db_models.daily_report import DailyReport
from app.utils.db_utils import row_to_dict
from app.utils.knowledge_utils import make_weekly_report_dates


class DailyReportRepository(IDailyReportRepository):
    def get_first(self) -> DailyReport:
        with SessionLocal() as db:
            daily_report = db.query(DailyReport).first()

        if not daily_report:
            raise HTTPException(status_code=422)

        return DailyReport(**row_to_dict(daily_report))

    def search_by_id(self, id: str) -> list[DailyReport]:
        with SessionLocal() as db:
            daily_report = db.query(DailyReport).filter(DailyReport.id == id).all()

        if not daily_report:
            raise HTTPException(status_code=422)

        return [DailyReport(**row_to_dict(daily_report)) for daily_report in daily_report]

    def find_by_date(self, date: str) -> list[DailyReport]:
        with SessionLocal() as db:
            daily_report = db.query(DailyReport).filter(DailyReport.date == date).all()

        if not daily_report:
            raise HTTPException(status_code=422)

        return [DailyReport(**row_to_dict(daily_report)) for daily_report in daily_report]

    def create(self, daily_report: DailyReport):
        with SessionLocal() as db:
            db.add(daily_report)
            db.commit()

    def get_weekly_report_contexts(self, end_date:str) -> tuple[str, list[str]]:
        datesToFetch = make_weekly_report_dates(end_date)

        with SessionLocal() as db:
            rows = db.query(DailyReport).filter(DailyReport.date.in_(datesToFetch)).all()

        data = [row_to_dict(row) for row in rows]

        market_analysis_ids = [row["id"] for row in data]

        contexts = ""
        for row in data:
            contexts += f"<document><date>{row['date']}</date><content>{row['content']}</content></document>"

        return contexts, market_analysis_ids