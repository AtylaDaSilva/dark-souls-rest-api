from pathlib import Path
from unittest import result
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from src.db.models import Base, Weapon


class DarkSoulsDBAPI:
    def __init__(self):
        root_dir = Path("db").resolve()
        root_dir.mkdir(parents=True, exist_ok=True)
        self.DB_PATH = root_dir / "dark-souls-api.db"
        self.ENGINE = create_engine(f"sqlite:///{self.DB_PATH}", echo=True)
        self.DB_SESSION = sessionmaker(self.ENGINE)
        Base.metadata.create_all(self.ENGINE)

    def insert(self, obj: Base | list[Base]):
        with self.DB_SESSION() as session:
            try:
                if isinstance(obj, list):
                    session.add_all(obj)
                else:
                    session.add(obj)
                session.commit()
            except:
                session.rollback()
                raise

    def fetch_weapons(self):
        with self.DB_SESSION() as session:
            return session.scalars(select(Weapon)).all()
