from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey
from sqlalchemy import inspect


class Base(DeclarativeBase):
    @classmethod
    def get_fields(cls):
        return inspect(cls).columns.keys()


class WeaponClass(Base):
    __tablename__ = "weapon_classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class Weapon(Base):
    __tablename__ = "weapons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    weapon_class_id: Mapped[int] = mapped_column(
        ForeignKey("weapon_classes.id"), nullable=False
    )
    base_atk: Mapped[int] = mapped_column(nullable=False)
    weight: Mapped[float] = mapped_column(nullable=False)
    durability: Mapped[int] = mapped_column(nullable=False)
    stability: Mapped[int] = mapped_column(nullable=False)
    req_str: Mapped[str] = mapped_column(String(1), nullable=False)
    req_dex: Mapped[str] = mapped_column(String(1), nullable=False)
    req_int: Mapped[str] = mapped_column(String(1), nullable=False)
    req_fth: Mapped[str] = mapped_column(String(1), nullable=False)
    scal_str: Mapped[str] = mapped_column(String(1), nullable=False)
    scal_dex: Mapped[str] = mapped_column(String(1), nullable=False)
    scal_int: Mapped[str] = mapped_column(String(1), nullable=False)
    scal_fth: Mapped[str] = mapped_column(String(1), nullable=False)

    def __repr__(self):
        return f"<Weapon name='{self.name}', id='{self.id}'>"
