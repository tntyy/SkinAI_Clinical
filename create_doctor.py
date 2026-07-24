from werkzeug.security import generate_password_hash

from app import create_app
from app.database.db import db
from app.models.user import User

app = create_app()

with app.app_context():

    doctor = User.query.filter_by(username="doctor").first()

    if doctor:
        print("Doctor already exists.")
    else:

        doctor = User(
            username="doctor",
            password_hash=generate_password_hash("Doctor@123"),
            role="doctor",
            is_active=True
        )

        db.session.add(doctor)
        db.session.commit()

        print("Doctor created successfully.")