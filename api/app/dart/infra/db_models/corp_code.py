from datetime import datetime

from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class DartCorpCode(Base):
    __tablename__ = "dart_corp_code"

    id: Mapped[str] = mapped_column(String(191), primary_key=True)
    corp_code: Mapped[str] = mapped_column(Text(), nullable=False)
    corp_name: Mapped[str] = mapped_column(Text(), nullable=False)
    corp_eng_name: Mapped[str] = mapped_column(Text(), nullable=False)
    stock_code: Mapped[str] = mapped_column(Text(), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
