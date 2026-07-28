from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.file import FileRequired
from wtforms import SubmitField


class UploadImageForm(FlaskForm):

    image = FileField(
        "Ảnh tổn thương",
        validators=[
            FileRequired()
        ]
    )

    submit = SubmitField(
        "Upload"
    )