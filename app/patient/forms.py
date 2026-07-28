from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    SelectField
)

from wtforms.validators import (
    DataRequired,
    Length,
    Optional,
    NumberRange
)


class PatientForm(FlaskForm):

    fullname = StringField(

        "Họ tên",

        validators=[
            DataRequired(),
            Length(max=100)
        ]
    )

    gender = SelectField(

        "Giới tính",

        choices=[

            ("male", "Nam"),

            ("female", "Nữ"),

            ("other", "Khác")

        ]
    )

    birth_year = IntegerField(

        "Năm sinh",

        validators=[

            Optional(),

            NumberRange(
                min=1900,
                max=2100
            )

        ]
    )

    phone = StringField(

        "Số điện thoại",

        validators=[

            Optional(),

            Length(max=20)

        ]
    )

    submit = SubmitField("Lưu")