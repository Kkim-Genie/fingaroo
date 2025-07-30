from datetime import datetime

from sqlalchemy import String, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column
from pgvector.sqlalchemy import Vector

from app.database import Base


class Embeddings(Base):
    __tablename__ = "embeddings"

    id: Mapped[str] = mapped_column(String(191), primary_key=True)
    date: Mapped[str] = mapped_column(Text(), nullable=True)
    origin_id: Mapped[str] = mapped_column(String(191), nullable=False)
    origin_type: Mapped[str] = mapped_column(String(50), nullable=False)
    content: Mapped[str] = mapped_column(Text(), nullable=True)
    embedding = mapped_column(Vector(1024), nullable=False)