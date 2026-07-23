from flask import Blueprint

ai = Blueprint(
    "ai",
    __name__,
    url_prefix="/ai"
)

from app.ai import routes