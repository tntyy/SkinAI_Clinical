from flask_wtf import FlaskForm
from wtforms import (
    IntegerField,
    SelectField,
    StringField,
    TextAreaField,
    SubmitField
)
from wtforms.validators import Optional


class MetadataForm(FlaskForm):

    age = IntegerField(
        "Tuổi",
        validators=[Optional()]
    )

    gender = SelectField(
        "Giới tính",
        choices=[
            ("male", "Nam"),
            ("female", "Nữ"),
            ("other", "Khác")
        ]
    )

    lesion_location = StringField(
        "Vị trí tổn thương"
    )

    skin_type = StringField(
        "Loại da"
    )

    device = StringField(
        "Thiết bị chụp"
    )

    note = TextAreaField(
        "Ghi chú"
    )

    submit = SubmitField(
        "Lưu Metadata"
    )