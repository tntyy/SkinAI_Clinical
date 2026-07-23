from flask import Blueprint

auth = Blueprint(
    "database",
    __name__,
    url_prefix="/database"
)

from app.auth import routes