from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    IntegerField,
    TextAreaField,
    SelectField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Optional,
    Length
)



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

class PatientForm(FlaskForm):

    fullname = StringField(
        "Họ và tên",
        validators=[
            DataRequired(
                message="Vui lòng nhập họ và tên."
            ),
            Length(
                max=100
            )
        ]
    )

    gender = SelectField(
        "Giới tính",
        choices=[
            ("", "Không xác định"),
            ("Nam", "Nam"),
            ("Nữ", "Nữ"),
            ("Khác", "Khác")
        ],
        validators=[
            Optional()
        ]
    )

    birth_year = IntegerField(
        "Năm sinh",
        validators=[
            Optional()
        ]
    )

    phone = StringField(
        "Số điện thoại",
        validators=[
            Optional(),
            Length(max=20)
        ]
    )

    drug_allergies = TextAreaField(
        "Dị ứng thuốc",
        validators=[
            Optional()
        ]
    )

    chronic_diseases = TextAreaField(
        "Bệnh nền",
        validators=[
            Optional()
        ]
    )

    hereditary_diseases = TextAreaField(
        "Bệnh di truyền",
        validators=[
            Optional()
        ]
    )

    submit = SubmitField(
        "Lưu thông tin"
    )