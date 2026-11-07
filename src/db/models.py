from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, ForeignKey


class Base(DeclarativeBase):
    pass


class WeaponClass(Base):
    __tablename__ = "weapon_classes"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)


class Weapon(Base):
    __tablename__ = "weapons"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    weapon_class_id: Mapped[int] = mapped_column(ForeignKey("weapon_classes.id"))

    def __repr__(self):
        return f"<Weapon name='{self.name}', id='{self.id}'>"
