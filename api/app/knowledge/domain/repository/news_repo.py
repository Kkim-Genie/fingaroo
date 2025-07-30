from abc import ABCMeta, abstractmethod
from app.knowledge.infra.db_models.news import News


class INewsRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_first(self) -> News:
        raise NotImplementedError

    @abstractmethod
    def search_by_id(self, id: str) -> list[News]:
        raise NotImplementedError

    @abstractmethod
    def find_by_date(self, date: str) -> list[News]:
        raise NotImplementedError

    @abstractmethod
    def get_latest_news(self, type: str) -> News:
        raise NotImplementedError

    @abstractmethod
    def create_news(self, news: list[News]):
        raise NotImplementedError

    @abstractmethod
    def get_daily_report_contexts(self, date:str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_weekly_report_contexts(self, end_date:str) -> tuple[str, list[str]]:
        raise NotImplementedError
