from abc import ABCMeta, abstractmethod

from app.knowledge.infra.db_models.daily_market_condition import DailyMarketCondition


class IDailyMarketConditionRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_first(self) -> DailyMarketCondition:
        raise NotImplementedError

    @abstractmethod
    def search_by_id(self, id: str) -> list[DailyMarketCondition]:
        raise NotImplementedError

    @abstractmethod
    def find_by_date(self, date: str) -> list[DailyMarketCondition]:
        raise NotImplementedError

    @abstractmethod
    def create(self, daily_market_condition: DailyMarketCondition):
        raise NotImplementedError

    @abstractmethod
    def get_weekly_report_contexts(self, end_date:str) -> tuple[str, list[str]]:
        raise NotImplementedError