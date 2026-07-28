from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash

from flask_login import login_required

from app.lesion import lesion

from app.lesion.forms import UploadImageForm
from app.lesion.services import LesionService
from app.lesion.repositories import LesionRepository


@lesion.route("/exam/<int:exam_id>")
@login_required
def list_images(exam_id):

    images = LesionRepository.get_by_exam(
        exam_id
    )

    return render_template(
        "lesion/list.html",
        images=images,
        exam_id=exam_id
    )


@lesion.route(
    "/exam/<int:exam_id>/upload",
    methods=["GET", "POST"]
)
@login_required
def upload_image(exam_id):

    form = UploadImageForm()

    if form.validate_on_submit():

        LesionService.upload(
            form,
            exam_id
        )

        flash(
            "Upload thành công.",
            "success"
        )

        return redirect(
            url_for(
                "lesion.list_images",
                exam_id=exam_id
            )
        )

    return render_template(
        "lesion/upload.html",
        form=form
    )