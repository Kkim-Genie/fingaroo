from sqlalchemy import DateTime, String, Text, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

from app.database import Base


class InvestLog(Base):
    __tablename__ = "invest_log"

    id: Mapped[str] = mapped_column(String(191), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(50), nullable=False)
    date: Mapped[str] = mapped_column(String(50), nullable=False)
    stock_code: Mapped[str] = mapped_column(Text, nullable=False)
    stock_name: Mapped[str] = mapped_column(Text, nullable=False)
    action: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    reason: Mapped[str] = mapped_column(Text, nullable=False)
    amount_ratio: Mapped[float] = mapped_column(Float, nullable=False)
    profit: Mapped[int] = mapped_column(Integer, nullable=False)
    profit_ratio: Mapped[float] = mapped_column(Float, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
