from flask_wtf import FlaskForm
from wtforms import (
    StringField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import DataRequired


class ExaminationForm(FlaskForm):

    chief_complaint = StringField(
        "Triệu chứng",
        validators=[DataRequired()]
    )

    note = TextAreaField(
        "Ghi chú"
    )

    submit = SubmitField(
        "Tạo lần khám"
    )