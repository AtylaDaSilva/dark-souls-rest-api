from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, inspect
from sqlalchemy.orm import DeclarativeBase
from pathlib import Path
from src.functions import serialize

# Init app and database
app = Flask(__name__)

root_dir = Path("db").resolve()
root_dir.mkdir(parents=True, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{root_dir / "dark-souls-api.db"}"


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
db.init_app(app)

# Create DB schema
with app.app_context():
    db.create_all()


# Define models
class Weapon(db.Model):
    __tablename__ = "weapons"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Weapon name='{self.name}', id='{self.id}'>"


# Routes
@app.route("/")
def main():
    return "<h1>Hello world!</h1>"


@app.route("/weapons", methods=["GET"])
def weapons():
    with db.session() as session:
        result = []
        for weap in session.execute(select(Weapon)).scalars().all():
            result.append(serialize(weap))
        return result
