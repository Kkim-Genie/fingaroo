from fastapi import HTTPException
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.knowledge.domain.repository.weekly_report_repo import IWeeklyReportRepository
from app.knowledge.infra.db_models.weekly_report import WeeklyReport
from app.utils.db_utils import row_to_dict
from app.utils.knowledge_utils import make_weekly_report_dates


class WeeklyReportRepository(IWeeklyReportRepository):
    def get_first(self) -> WeeklyReport:
        with SessionLocal() as db:
            weekly_report = db.query(WeeklyReport).first()

        if not weekly_report:
            raise HTTPException(status_code=422)

        return WeeklyReport(**row_to_dict(weekly_report))

    def search_by_id(self, id: str) -> list[WeeklyReport]:
        with SessionLocal() as db:
            weekly_report = db.query(WeeklyReport).filter(WeeklyReport.id == id).all()

        return [WeeklyReport(**row_to_dict(weekly_report)) for weekly_report in weekly_report]

    def search_by_start_date(self, start_date: str) -> list[WeeklyReport]:
        with SessionLocal() as db:
            weekly_report = db.query(WeeklyReport).filter(WeeklyReport.start_date == start_date).all()

        return [WeeklyReport(**row_to_dict(weekly_report)) for weekly_report in weekly_report]

    def search_by_end_date(self, end_date: str) -> list[WeeklyReport]:
        with SessionLocal() as db:
            weekly_report = db.query(WeeklyReport).filter(WeeklyReport.end_date == end_date).order_by(WeeklyReport.end_date.desc()).first()

        return WeeklyReport(**row_to_dict(weekly_report))

    def create(self, weekly_report: WeeklyReport):
        with SessionLocal() as db:
            db.add(weekly_report)
            db.commit()