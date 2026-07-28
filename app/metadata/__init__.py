from flask import Blueprint

metadata = Blueprint(
    "metadata",
    __name__,
    url_prefix="/metadata"
)

from app.metadata import routes