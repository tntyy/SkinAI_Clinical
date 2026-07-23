from app.database.db import db


class Disease(db.Model):
    __tablename__ = "diseases"

    disease_id = db.Column(db.Integer, primary_key=True)

    disease_code = db.Column(db.String(20), unique=True, nullable=False)

    disease_name = db.Column(db.String(100), nullable=False)

    disease_name_vi = db.Column(db.String(100), nullable=False)

    category = db.Column(db.String(50))

    overview = db.Column(db.Text)

    symptoms = db.Column(db.Text)

    causes = db.Column(db.Text)

    risk_factors = db.Column(db.Text)

    diagnosis = db.Column(db.Text)

    treatment = db.Column(db.Text)

    prevention = db.Column(db.Text)

    follow_up = db.Column(db.Text)

    common_locations = db.Column(db.Text)

    age_group = db.Column(db.String(100))

    gender_prevalence = db.Column(db.String(100))

    prevalence = db.Column(db.String(255))

    risk_level = db.Column(db.String(20))

    icd10_code = db.Column(db.String(20))

    reference_image = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        server_default=db.func.now()
    )