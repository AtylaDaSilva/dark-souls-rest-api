from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.models.base import Base


class Weapon(Base):
    __tablename__ = "WEAPONS"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
