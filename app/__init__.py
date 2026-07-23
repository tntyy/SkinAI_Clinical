from flask import Flask
from flask import redirect
from flask import url_for
from config import Config
from app.database.db import db, migrate
from flask_login import LoginManager

import app.models

from app.home.routes import home
from app.doctor.routes import doctor
from app.models.user import User
from app.auth import auth
from app.patient import patient
from app.examination import examination
from app.admin import admin

login_manager = LoginManager()
login_manager.login_view ='auth.login'
login_manager.login_message = "Vui lòng đăng nhập!"
login_manager.login_message_category = "warning"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app, db)

    app.register_blueprint(home)
    app.register_blueprint(doctor)
    app.register_blueprint(auth)
    app.register_blueprint(patient)
    app.register_blueprint(examination)
    app.register_blueprint(admin)

    login_manager.init_app(app)

    return app