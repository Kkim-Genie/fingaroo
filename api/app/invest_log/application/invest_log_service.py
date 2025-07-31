from datetime import datetime
from app.invest_log.domain.repository.invest_log_repo import IInvestLogRepository
from app.invest_log.domain.invest_log import InvestLog
from app.utils.id_utils import generate_nanoid


class InvestLogService:
    def __init__(
        self,
        invest_log_repo: IInvestLogRepository,
    ):
        self.invest_log_repo = invest_log_repo    

    def search_by_user_id(self, user_id: str) -> list[InvestLog]:
        return self.invest_log_repo.search_by_user_id(user_id)

    def find_by_id(self, invest_log_id: str) -> InvestLog:
        return self.invest_log_repo.find_by_id(invest_log_id)

    def create(self, user_id: str, date: str, stock_code: int, stock_name: str, action: str, amount: int, reason: str, amount_ratio: float, profit: int, profit_ratio: float, price: int):
        

        invest_log = InvestLog(
            id=generate_nanoid(),
            user_id=user_id,
            date=date,
            stock_code=stock_code,
            stock_name=stock_name,
            action=action,
            price=price,
            amount=amount,
            reason=reason,
            amount_ratio=amount_ratio,
            profit=profit,
            profit_ratio=profit_ratio,
            created_at=datetime.now()
        )
        return self.invest_log_repo.create_invest_log(invest_log)

    def update(self, invest_log: InvestLog):
        return self.invest_log_repo.update_invest_log(invest_log.id, invest_log)

    def delete(self, invest_log_id: str):
        return self.invest_log_repo.delete_invest_log(invest_log_id)
