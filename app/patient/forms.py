from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    IntegerField,
    SubmitField,
    SelectField,
    TextAreaField
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

    # ==============================
    # BỆNH SỬ
    # ==============================

    drug_allergies = TextAreaField(
        "Dị ứng thuốc",
        validators=[
            Optional()
        ],
        render_kw={
            "rows": 3,
            "placeholder": "Ví dụ: Penicillin, Amoxicillin..."
        }
    )

    chronic_diseases = TextAreaField(
        "Bệnh nền",
        validators=[
            Optional()
        ],
        render_kw={
            "rows": 3,
            "placeholder": "Ví dụ: Tiểu đường, cao huyết áp..."
        }
    )

    hereditary_diseases = TextAreaField(
        "Bệnh di truyền",
        validators=[
            Optional()
        ],
        render_kw={
            "rows": 3,
            "placeholder": "Ví dụ: Gia đình có tiền sử..."
        }
    )

    submit = SubmitField("Lưu")