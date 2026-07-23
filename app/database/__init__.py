from flask import Blueprint

database = Blueprint(
    "database",
    __name__,
    url_prefix="/database"
)

from app.auth import routes