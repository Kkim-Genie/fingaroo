from datetime import datetime

from sqlalchemy import String, DateTime, Text, ARRAY
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.database import Base


class News(Base):
    __tablename__ = "news"

    id: Mapped[str] = mapped_column(String(191), primary_key=True)
    title: Mapped[str] = mapped_column(Text(), nullable=True)
    link: Mapped[str] = mapped_column(Text(), nullable=True)
    date: Mapped[str] = mapped_column(Text(), nullable=True)
    content: Mapped[str] = mapped_column(Text(), nullable=False)
    type: Mapped[str] = mapped_column(Text(), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
