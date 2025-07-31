from fastapi import HTTPException
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.invest_log.domain.repository.invest_log_repo import IInvestLogRepository
from app.invest_log.infra.db_models.invest_log import InvestLog
from app.invest_log.domain.invest_log import InvestLog as InvestLogV0
from app.utils.db_utils import row_to_dict


class InvestLogRepository(IInvestLogRepository):
    def search_by_user_id(self, user_id: str) -> list[InvestLogV0]:
        with SessionLocal() as db:
            invest_logs = db.query(InvestLog).filter(InvestLog.user_id == user_id).all()

        # 데이터가 없으면 빈 리스트 반환 (오류가 아님)
        if not invest_logs:
            return []

        return [InvestLogV0(**row_to_dict(invest_log)) for invest_log in invest_logs]

    def create_invest_log(self, invest_log: InvestLogV0):
        with SessionLocal() as db:
            # domain 모델을 DB 모델로 변환
            db_invest_log = InvestLog(
                id=invest_log.id,
                user_id=invest_log.user_id,
                date=invest_log.date,
                stock_code=invest_log.stock_code,
                stock_name=invest_log.stock_name,
                action=invest_log.action,
                price=invest_log.price,
                amount=invest_log.amount,
                reason=invest_log.reason,
                amount_ratio=invest_log.amount_ratio,
                profit=invest_log.profit,
                profit_ratio=invest_log.profit_ratio,
                created_at=invest_log.created_at
            )
            db.add(db_invest_log)
            db.commit()

        return invest_log

    def update_invest_log(self, invest_log_id: str, invest_log: InvestLogV0):
        with SessionLocal() as db:
            db.query(InvestLog).filter(InvestLog.id == invest_log_id).update({
                "date": invest_log.date,
                "stock_code": invest_log.stock_code,
                "stock_name": invest_log.stock_name,
                "action": invest_log.action,
                "price": invest_log.price,
                "amount": invest_log.amount,
                "reason": invest_log.reason,
                "amount_ratio": invest_log.amount_ratio,
                "profit": invest_log.profit,
                "profit_ratio": invest_log.profit_ratio
            })
            db.commit()

        return invest_log

    def delete_invest_log(self, invest_log_id: str):
        with SessionLocal() as db:
            db.query(InvestLog).filter(InvestLog.id == invest_log_id).delete()
            db.commit()
