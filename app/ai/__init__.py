from flask import Blueprint

auth = Blueprint(
    "ai",
    __name__,
    url_prefix="/ai"
)

from app.ai import routes