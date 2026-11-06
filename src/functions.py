from sqlalchemy import inspect
from flask_sqlalchemy.model import Model
from typing import Any


def serialize(model: Model) -> dict[str, Any]:
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
