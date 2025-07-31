from sqlalchemy import String, Text, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class UserAsset(Base):
    __tablename__ = "user_asset"

    id: Mapped[str] = mapped_column(String(191), primary_key=True)
    user_id: Mapped[str] = mapped_column(String(50), nullable=False)
    stock_code: Mapped[str] = mapped_column(Text, nullable=False)
    stock_name: Mapped[str] = mapped_column(Text, nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
