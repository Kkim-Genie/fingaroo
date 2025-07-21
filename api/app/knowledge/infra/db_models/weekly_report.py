from datetime import datetime

from sqlalchemy import String, DateTime, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.database import Base


class WeeklyReport(Base):
    __tablename__ = "weekly_report"

    id: Mapped[str] = mapped_column(String(191), primary_key=True)
    start_date: Mapped[str] = mapped_column(Text(), nullable=True)
    end_date: Mapped[str] = mapped_column(Text(), nullable=True)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    market_analysis_ids: Mapped[list[str]] = mapped_column(ARRAY(String(191)), nullable=False)
    news_ids: Mapped[list[str]] = mapped_column(ARRAY(String(191)), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
