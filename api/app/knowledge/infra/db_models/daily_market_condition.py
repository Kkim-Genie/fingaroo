from datetime import datetime

from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.database import Base


class DailyMarketCondition(Base):
    __tablename__ = "daily_market_condition"

    id: Mapped[str] = mapped_column(String(191), primary_key=True)
    date: Mapped[str] = mapped_column(Text(), nullable=True)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
