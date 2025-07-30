from abc import ABCMeta, abstractmethod

from app.knowledge.infra.db_models.daily_report import DailyReport


class IDailyReportRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_first(self) -> DailyReport:
        raise NotImplementedError

    @abstractmethod
    def search_by_id(self, id: str) -> list[DailyReport]:
        raise NotImplementedError

    @abstractmethod
    def find_by_date(self, date: str) -> list[DailyReport]:
        raise NotImplementedError

    @abstractmethod
    def create(self, daily_report: DailyReport):
        raise NotImplementedError

    @abstractmethod
    def get_weekly_report_contexts(self, end_date:str) -> tuple[str, list[str]]:
        raise NotImplementedError