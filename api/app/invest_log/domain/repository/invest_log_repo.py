from abc import ABCMeta, abstractmethod
from app.invest_log.domain.invest_log import InvestLog


class IInvestLogRepository(metaclass=ABCMeta):
    @abstractmethod
    def search_by_user_id(self, user_id: str) -> list[InvestLog]:
        raise NotImplementedError

    @abstractmethod
    def create_invest_log(self, invest_log: InvestLog):
        raise NotImplementedError

    @abstractmethod
    def update_invest_log(self, invest_log_id: str, invest_log: InvestLog):
        raise NotImplementedError

    @abstractmethod
    def delete_invest_log(self, invest_log_id: str):
        raise NotImplementedError
