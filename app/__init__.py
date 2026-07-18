from flask import Flask
from flask import redirect
from flask import url_for
from config import Config
from app.database.db import db, migrate

import app.models

from app.home.routes import home
from app.doctor.routes import doctor


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)

    app.register_blueprint(home)
    app.register_blueprint(doctor)

    return app