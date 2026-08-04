from flask import render_template
from flask import redirect
from flask import url_for
from flask import flash
from flask import request

from flask_login import login_required

from app.lesion import lesion

from app.lesion.forms import UploadImageForm
from app.lesion.services import LesionService
import os

from app.ai.services import AIService
from app.doctor.services import DoctorReportService

@lesion.route("/exam/<int:exam_id>")
@login_required
def list_images(exam_id):

    images = LesionService.get_by_examination(
        exam_id
    )

    return render_template(
        "lesion/list.html",
        images=images,
        exam_id=exam_id
    )

@lesion.route("/detail/<int:image_id>")
@login_required
def detail(image_id):

    lesion = LesionService.get_by_id(image_id)

    if lesion is None:

        flash(
            "Không tìm thấy ảnh.",
            "danger"
        )

        return redirect(
            url_for("doctor.dashboard")
        )

    image_path = os.path.join(
        "app",
        "static",
        lesion.image_path
    )

    data = AIService.predict(
        image_path,
        lesion.image_id
    )

    report = DoctorReportService.get_report(
        lesion.exam_id
    )

    return render_template(
        "lesion/detail.html",
        lesion=lesion,
        results=data["results"],
        heatmap_path=data["heatmap_path"],
        overlay_path=data["overlay_path"],
        report=report
    )

@lesion.route(
    "/exam/<int:exam_id>/upload",
    methods=["GET","POST"]
)
@login_required
def upload_image(exam_id):

    form = UploadImageForm()

    if request.method == "POST":

        file = request.files.get("image")

        # Upload từ Camera
        if file:

            LesionService.upload_file(
                file,
                exam_id
            )

            return "OK", 200

        # Upload từ máy
        if form.validate_on_submit():

            LesionService.upload(
                form,
                exam_id
            )

            flash(
                "Upload thành công",
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
        form=form,
        exam_id=exam_id
    )

@lesion.route(
    "/delete/<int:image_id>",
    methods=["POST"]
)
@login_required
def delete_image(image_id):

    image = LesionService.get_by_id(image_id)

    if image is None:

        flash(
            "Không tìm thấy ảnh.",
            "danger"
        )

        return redirect(
            url_for("doctor.dashboard")
        )

    exam_id = image.exam_id

    LesionService.delete(image)

    flash(
        "Đã xóa ảnh.",
        "success"
    )

    return redirect(

        url_for(

            "lesion.list_images",

            exam_id=exam_id

        )

    )