from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from pathlib import Path
from src.db.utils.functions import (
    serialize,
    get_default_db_objects,
    populate_database,
    check_required_fields,
)
from src.db.utils.exceptions import MissingRequestFormItem
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


@app.errorhandler(400)
def resource_not_found(e):
    return jsonify(status_code=400, error=str(e)), 400


@app.errorhandler(500)
def internal_error(e):
    return jsonify(status_code=500, error=f"Internal Error: {str(e)}"), 500


# Routes
@app.route("/")
def main():
    global flg_populate_db
    if flg_populate_db is True:
        populate_database(db.session, get_default_db_objects())
        flg_populate_db = False
    return "<h1>Welcome to the Dark Souls REST API!</h1>"


@app.route("/weapons", methods=["GET", "POST"])
def weapons():
    match request.method:
        case "GET":
            with db.session() as session:
                result = []
                for weap in session.execute(select(Weapon)).scalars().all():
                    result.append(weap.serialize())
                return result
        case "POST":
            try:
                check_required_fields(request.form, Weapon, exclude=["id"])
                new_weap = Weapon(**request.form)
                try:
                    with db.session() as session:
                        session.add(new_weap)
                except Exception as e:
                    session.rollback()
                    abort(500, e)

            except MissingRequestFormItem as item:
                abort(400, description=f"Missing '{item}' in request body.")
            return {}
        case _:
            abort(400)


@app.route("/weapons/id/<int:weapon_id>", methods=["GET"])
def weapon_id(weapon_id: int):
    with db.session() as session:
        record = session.execute(select(Weapon).where(Weapon.id == weapon_id)).first()
        return serialize(record[0]) if record else {}


@app.route("/weapons/classes", methods=["GET"])
def weapon_classes():
    with db.session() as session:
        result = []
        for weap_class in session.execute(select(WeaponClass)).scalars().all():
            result.append(serialize(weap_class))
        return result


@app.route("/weapons/classes/id/<int:weapon_cls_id>", methods=["GET"])
def weapon_class_id(weapon_cls_id: int):
    with db.session() as session:
        record = session.execute(
            select(WeaponClass).where(WeaponClass.id == weapon_cls_id)
        ).first()
        return serialize(record[0]) if record else {}
