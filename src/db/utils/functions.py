from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
from typing import Any, Callable
from src.db.models import WeaponClass, Weapon


def get_default_db_objects() -> list[DeclarativeBase]:
    return [
        WeaponClass(name="Straightsword"),
        WeaponClass(name="Dagger"),
        Weapon(name="Longsword", weapon_class_id=1),
        Weapon(name="Shortsword", weapon_class_id=1),
        Weapon(name="Dagger", weapon_class_id=2),
        Weapon(name="Bandit's Dagger", weapon_class_id=2),
    ]


def populate_database(db_session: Callable, objs: list):
    with db_session() as session:
        try:
            session.add_all(objs)
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()


def serialize(model: DeclarativeBase) -> dict[str, Any]:
    """Serializes a SQLAlchemy/Flask-SQLAlchemy model into a python `dict`.

    Args:
        model (Model): A SQLAlchemy or Flask-SQLAlchemy model (a subclass of sqlalchemy.orm.DeclarativeBase)

    Returns:
        dict[str, Any]: A `dict` representation of *model*, containing only its manually-set properties.
    """
    serialized = {}
    fields: list[str] = inspect(model.__class__).columns.keys()
    for f in fields:
        serialized[f] = getattr(model, f)
    return serialized
