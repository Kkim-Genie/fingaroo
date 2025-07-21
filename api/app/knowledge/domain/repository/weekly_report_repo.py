from abc import ABCMeta, abstractmethod
from app.knowledge.infra.db_models.weekly_report import WeeklyReport


class IWeeklyReportRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_first(self) -> WeeklyReport:
        raise NotImplementedError

    @abstractmethod
    def search_by_id(self, id: str) -> list[WeeklyReport]:
        raise NotImplementedError

    @abstractmethod
    def search_by_start_date(self, start_date: str) -> list[WeeklyReport]:
        raise NotImplementedError

    @abstractmethod
    def search_by_end_date(self, start_date: str) -> list[WeeklyReport]:
        raise NotImplementedError

    @abstractmethod
    def create(self, weekly_report: WeeklyReport):
        raise NotImplementedError