from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path
from src.functions import serialize

# Init app and database
app = Flask(__name__)

root_dir = Path("db").resolve()
root_dir.mkdir(parents=True, exist_ok=True)
DB_PATH = root_dir / "dark-souls-api.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)


# Models
class WeaponClass(db.Model):
    __tablename__ = "weapon_classes"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    weapons = db.relationship("Weapon", back_populates="weapon_classes")


class Weapon(db.Model):
    __tablename__ = "weapons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    weapon_class_id = db.Column(
        db.Integer, db.ForeignKey("weapon_classes.id"), nullable=False
    )
    weapon_classes = db.relationship("WeaponClass", back_populates="weapons")

    def __repr__(self):
        return f"<Weapon name='{self.name}', id='{self.id}'>"


# Create DB schema
flg_populate_db = False
with app.app_context():
    if not DB_PATH.exists():
        flg_populate_db = True
    db.create_all()


# Routes
@app.route("/")
def main():
    global flg_populate_db
    if flg_populate_db is True:
        with db.session() as session:
            try:
                weapon_classes = [
                    WeaponClass(name="Straightsword"),
                    WeaponClass(name="Dagger"),
                ]
                with db.session() as session:
                    session.add_all(weapon_classes)
                    session.commit()
                flg_populate_db = False
            except Exception as e:
                print(e)
                session.rollback()
    return "<h1>Hello world!</h1>"


@app.route("/weapons", methods=["GET"])
def weapons():
    with db.session() as session:
        result = []
        for weap in session.execute(select(Weapon)).scalars().all():
            result.append(serialize(weap))
        return result


@app.route("/weapons/classes", methods=["GET"])
def weapon_classes():
    with db.session() as session:
        result = []
        for weap_class in session.execute(select(WeaponClass)).scalars().all():
            result.append(serialize(weap_class))
        return result
