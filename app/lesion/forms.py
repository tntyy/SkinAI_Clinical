from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.file import FileRequired
from flask_wtf.file import FileAllowed

from wtforms import SubmitField


class UploadImageForm(FlaskForm):

    image = FileField(

        "Ảnh tổn thương",

        validators=[

            FileRequired(),

            FileAllowed(

                ["jpg", "jpeg", "png"],

                "Chỉ cho phép JPG hoặc PNG"

            )

        ]

    )

    submit = SubmitField("Upload")