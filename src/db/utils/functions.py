from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase
from typing import Any, Callable
from itertools import chain
from src.db.models import WeaponClass, Weapon


def get_default_db_objects() -> list[DeclarativeBase]:
    # fmt: off
    objs = [
        [
            WeaponClass(name="Straight Sword"),     # 1
            WeaponClass(name="Thrusting Sword"),    # 2
            WeaponClass(name="Curved Sword"),       # 3
            WeaponClass(name="Axe"),                # 4
            WeaponClass(name="Curved Greatsword"),  # 5
            WeaponClass(name="Great Hammer"),       # 6
            WeaponClass(name="Greatsword"),         # 7
            WeaponClass(name="Great Axe"),          # 8
            WeaponClass(name="Hammer"),             # 9
            WeaponClass(name="Katana"),             # 10
        ],
        [
            Weapon(
                name="Longsword",
                weapon_class_id=1,
                base_atk=80,
                weight=3,
                durability=200,
                stability=32,
                req_str=10,
                req_dex=10,
                req_int=0,
                req_fth=0,
                scal_str="C",
                scal_dex="C",
                scal_int="",
                scal_fth="",
            ),
            Weapon(
                name="Rapier",
                weapon_class_id=2,
                base_atk=73,
                weight=1.5,
                durability=150,
                stability=22,
                req_str=5,
                req_dex=12,
                req_int=0,
                req_fth=0,
                scal_str="D",
                scal_dex="C",
                scal_int="",
                scal_fth="",
            ),
            Weapon(
                name="Scimitar",
                weapon_class_id=3,
                base_atk=80,
                weight=1.5,
                durability=160,
                stability=30,
                req_str=7,
                req_dex=13,
                req_int=0,
                req_fth=0,
                scal_str="E",
                scal_dex="B",
                scal_int="",
                scal_fth="",
            ),
            Weapon(
                name="Battle Axe",
                weapon_class_id=4,
                base_atk=95,
                weight=4,
                durability=250,
                stability=36,
                req_str=12,
                req_dex=8,
                req_int=0,
                req_fth=0,
                scal_str="C",
                scal_dex="D",
                scal_int="",
                scal_fth="",
            ),
            Weapon(
                name="Murakumo",
                weapon_class_id=5,
                base_atk=113,
                weight=12,
                durability=180,
                stability=36,
                req_str=28,
                req_dex=13,
                req_int=0,
                req_fth=0,
                scal_str="E",
                scal_dex="B",
                scal_int="",
                scal_fth="",
            ),
            Weapon(
                name="Great Club",
                weapon_class_id=6,
                base_atk=135,
                weight=12,
                durability=250,
                stability=32,
                req_str=28,
                req_dex=0,
                req_int=0,
                req_fth=0,
                scal_str="B",
                scal_dex="",
                scal_int="",
                scal_fth="",
            ),
            Weapon(
                name="Claymore",
                weapon_class_id=7,
                base_atk=103,
                weight=6,
                durability=200,
                stability=38,
                req_str=16,
                req_dex=10,
                req_int=0,
                req_fth=0,
                scal_str="C",
                scal_dex="C",
                scal_int="",
                scal_fth="",
            ),
            Weapon(
                name="Greataxe",
                weapon_class_id=8,
                base_atk=140,
                weight=14,
                durability=230,
                stability=38,
                req_str=32,
                req_dex=8,
                req_int=0,
                req_fth=0,
                scal_str="C",
                scal_dex="E",
                scal_int="",
                scal_fth="",
            ),
            Weapon(
                name="Mace",
                weapon_class_id=9,
                base_atk=91,
                weight=4,
                durability=250,
                stability=30,
                req_str=12,
                req_dex=0,
                req_int=0,
                req_fth=0,
                scal_str="B",
                scal_dex="",
                scal_int="",
                scal_fth="",
            ),
            Weapon(
                name="Uchigatana",
                weapon_class_id=10,
                base_atk=90,
                weight=5,
                durability=80,
                stability=30,
                req_str=14,
                req_dex=14,
                req_int=0,
                req_fth=0,
                scal_str="",
                scal_dex="B",
                scal_int="",
                scal_fth="",
            ),
        ]
    ]
    # fmt: on
    return list(chain.from_iterable(objs))


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
