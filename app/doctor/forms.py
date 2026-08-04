from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired


class DoctorReviewForm(FlaskForm):

    diagnosis = StringField(
        "Chẩn đoán",
        validators=[DataRequired()]
    )

    treatment = TextAreaField(
        "Điều trị"
    )

    note = TextAreaField(
        "Ghi chú"
    )

    submit = SubmitField(
        "Xác nhận kết quả"
    )