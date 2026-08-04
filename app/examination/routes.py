from flask import (
    render_template,
    redirect,
    url_for,
    flash
)

from flask_login import login_required

from app.examination import examination

from app.examination.forms import ExaminationForm
from app.examination.services import ExaminationService


####################################################
# Tạo lần khám
####################################################

@examination.route(
    "/create/<int:patient_id>",
    methods=["GET", "POST"]
)
@login_required
def create_examination(patient_id):

    form = ExaminationForm()

    if form.validate_on_submit():

        exam = ExaminationService.create(
            patient_id,
            form
        )

        flash(
            "Đã tạo lần khám.",
            "success"
        )

        return redirect(

            url_for(

                "examination.detail",

                exam_id=exam.exam_id

            )

        )

    return render_template(

        "examination/create.html",

        form=form,

        patient_id=patient_id

    )


####################################################
# Danh sách lần khám
####################################################

@examination.route("/patient/<int:patient_id>")
@login_required
def list_examinations(patient_id):

    examinations = ExaminationService.get_patient_examinations(
        patient_id
    )

    return render_template(

        "examination/list.html",

        examinations=examinations,

        patient_id=patient_id

    )


####################################################
# Chi tiết lần khám
####################################################

@examination.route("/<int:exam_id>")
@login_required
def detail(exam_id):

    examination_data = ExaminationService.get_detail(
        exam_id
    )

    if examination_data is None:

        flash(
            "Không tìm thấy lần khám.",
            "danger"
        )

        return redirect(
            url_for("doctor.dashboard")
        )

    return render_template(

        "examination/detail.html",

        examination=examination_data

    )
####################################################
# Sửa lần khám
####################################################

@examination.route(
    "/<int:exam_id>/edit",
    methods=["GET", "POST"]
)
@login_required
def edit(exam_id):

    exam = ExaminationService.get_by_id(exam_id)

    if exam is None:

        flash(
            "Không tìm thấy lần khám.",
            "danger"
        )

        return redirect(
            url_for("doctor.dashboard")
        )

    form = ExaminationForm(obj=exam)

    if form.validate_on_submit():

        ExaminationService.update(
            exam,
            form
        )

        flash(
            "Đã cập nhật lần khám.",
            "success"
        )

        return redirect(
            url_for(
                "examination.detail",
                exam_id=exam.exam_id
            )
        )

    return render_template(

        "examination/edit.html",

        form=form,

        examination=exam

    )
####################################################
# Xóa lần khám
####################################################

@examination.route(
    "/<int:exam_id>/delete",
    methods=["POST"]
)
@login_required
def delete(exam_id):

    exam = ExaminationService.get_by_id(exam_id)

    if exam is None:

        flash(
            "Không tìm thấy lần khám.",
            "danger"
        )

        return redirect(
            url_for("doctor.dashboard")
        )

    patient_id = exam.patient_id

    ExaminationService.delete(exam)

    flash(
        "Đã xóa lần khám.",
        "success"
    )

    return redirect(

        url_for(

            "examination.list_examinations",

            patient_id=patient_id

        )

    )