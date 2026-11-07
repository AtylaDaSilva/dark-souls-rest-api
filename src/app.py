from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from pathlib import Path
from src.db.utils.functions import serialize, get_default_db_objects, populate_database
from src.db.models import Base, Weapon, WeaponClass

# Init app and database
app = Flask(__name__)

root_dir = Path("db").resolve()
root_dir.mkdir(parents=True, exist_ok=True)
DB_PATH = root_dir / "dark-souls-api.db"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_PATH}"

db = SQLAlchemy(model_class=Base)
db.init_app(app)

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
        populate_database(db.session, get_default_db_objects())
        flg_populate_db = False
    return "<h1>Welcome to the Dark Souls REST API!</h1>"


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
