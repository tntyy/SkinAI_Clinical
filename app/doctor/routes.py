from flask import (
    render_template,
    redirect,
    url_for,
    flash,
    send_file,
    request,
    jsonify
)

from flask_login import (
    login_required,
    current_user
)

from werkzeug.security import (
    check_password_hash,
    generate_password_hash
)

from app.ai.grok_service import GrokService

from app.database.db import db

from app.doctor import doctor

from app.doctor.forms import DoctorReviewForm

from app.doctor.services import DoctorReportService

from app.doctor.dashboard_service import DashboardService

from app.ai.repositories import AIRepository

from app.lesion.repositories import (
    LesionImageRepository
)

from app.models.report_prediction_ref import (
    ReportPredictionRef
)

from app.doctor.pdf_service import PDFService

from app.doctor.repositories import (
    DoctorReportRepository
)

from app.doctor.icd10_mapping import (
    get_vietnamese_name,
    get_vietnamese_description
)


# ==========================================================
# DASHBOARD
# ==========================================================

@doctor.route("/dashboard")
@login_required
def dashboard():

    data = DashboardService.get_dashboard()

    return render_template(
        "doctor/dashboard.html",
        data=data
    )


# ==========================================================
# PATIENTS
# ==========================================================

@doctor.route("/patients")
@login_required
def patients():

    return render_template(
        "doctor/patients.html"
    )


# ==========================================================
# LESIONS
# ==========================================================

@doctor.route("/lesions")
@login_required
def lesions():

    return render_template(
        "doctor/lesions.html"
    )


# ==========================================================
# AI
# ==========================================================

@doctor.route("/ai")
@login_required
def ai():

    return render_template(
        "doctor/ai.html"
    )

# ==========================================================
# SKINAI CHAT
# ==========================================================

@doctor.route(
    "/chat",
    methods=["POST"]
)
@login_required
def chat():

    try:

        data = request.get_json(silent=True) or {}

        message = (
            data.get("message", "")
            .strip()
        )

        if not message:

            return jsonify({
                "success": False,
                "message": "Vui lòng nhập câu hỏi."
            }), 400

        # ==========================================
        # LẤY KẾT QUẢ AI MỚI NHẤT
        # ==========================================

        context = (
            AIRepository
            .get_latest_prediction_for_chat()
        )

        if not context:

            return jsonify({
                "success": False,
                "message": (
                    "Hiện tại chưa có kết quả AI "
                    "để hỗ trợ trả lời."
                )
            }), 404

        # ==========================================
        # GỌI GROK
        # ==========================================

        reply = GrokService.chat(
            message,
            context
        )

        # ==========================================
        # RESPONSE
        # ==========================================

        return jsonify({

            "success": True,

            "reply": reply,

            "context": {

                "disease":
                    context.get("disease"),

                "prediction":
                    context.get("prediction"),

                "confidence":
                    context.get("confidence"),

                "icd10":
                    context.get("icd10"),

                "risk":
                    context.get("risk")

            }

        })

    except Exception as e:

        print(
            "❌ GROK CHAT ERROR:",
            repr(e)
        )

        return jsonify({

            "success": False,

            "message":
                "Không thể kết nối với SkinAI Assistant.",

            "error":
                str(e)

        }), 500


# ==========================================================
# EXPLAIN
# ==========================================================

@doctor.route("/explain")
@login_required
def explain():

    return render_template(
        "doctor/explain.html"
    )


# ==========================================================
# HISTORY
# ==========================================================

@doctor.route("/history")
@login_required
def history():

    return render_template(
        "doctor/history.html"
    )


# ==========================================================
# REPORTS
# ==========================================================

@doctor.route("/reports")
@login_required
def reports():

    reports = (
        DoctorReportRepository
        .get_all()
    )

    return render_template(
        "doctor/report.html",
        reports=reports
    )


# ==========================================================
# EXPORT REPORT PDF
#
# /doctor/reports/19/export-pdf
# ==========================================================

@doctor.route(
    "/reports/<int:report_id>/export-pdf"
)
@login_required
def export_report_pdf(report_id):

    # ======================================================
    # 1. REPORT
    # ======================================================

    report = (
        DoctorReportRepository
        .get_by_id(
            report_id
        )
    )

    if report is None:

        flash(
            "Không tìm thấy báo cáo.",
            "danger"
        )

        return redirect(
            url_for(
                "doctor.reports"
            )
        )

    # ======================================================
    # 2. EXAM
    # ======================================================

    exam = report.examination

    if exam is None:

        flash(
            "Không tìm thấy thông tin ca khám.",
            "danger"
        )

        return redirect(
            url_for(
                "doctor.reports"
            )
        )

    # ======================================================
    # 3. PATIENT
    # ======================================================

    patient = exam.patient

    # ======================================================
    # 4. DOCTOR
    # ======================================================

    doctor = report.doctor

    # ======================================================
    # 5. LESION
    # ======================================================

    lesion = (
        LesionImageRepository
        .get_first_by_exam(
            exam.exam_id
        )
    )

    if lesion is None:

        flash(
            "Không tìm thấy ảnh tổn thương.",
            "danger"
        )

        return redirect(
            url_for(
                "doctor.reports"
            )
        )

    # ======================================================
    # 6. AI PREDICTION
    # ======================================================

    prediction_ref = (

        ReportPredictionRef.query

        .filter_by(
            report_id=report.report_id
        )

        .first()

    )

    prediction = None

    results = []

    heatmap = None

    if prediction_ref:

        prediction = (
            prediction_ref.prediction
        )

        if prediction:

            results = (
                AIRepository
                .get_prediction_details(
                    prediction.prediction_id
                )
            )

            heatmap = (
                AIRepository
                .get_heatmap(
                    prediction.prediction_id
                )
            )

    # ======================================================
    # DEBUG
    # ======================================================

    print(
        "=========================================="
    )

    print(
        "PDF REPORT:",
        report.report_id
    )

    print(
        "LESION IMAGE:",
        lesion.image_path
    )

    print(
        "PREDICTION:",
        prediction
    )

    print(
        "AI RESULTS:",
        results
    )

    print(
        "HEATMAP:",
        heatmap
    )

    if heatmap:

        print(
            "HEATMAP PATH:",
            heatmap.heatmap_path
        )

        print(
            "OVERLAY PATH:",
            heatmap.overlay_path
        )

    print(
        "=========================================="
    )

    # ======================================================
    # 7. GENERATE PDF
    # ======================================================

    pdf = PDFService.generate_pdf({

        "patient": patient,

        "doctor": doctor,

        "exam": exam,

        "lesion": lesion,

        "lesion_image": lesion.image_path,

        "prediction": prediction,

        "results": results,

        "report": report,

        "heatmap": heatmap

    })

    # ======================================================
    # 8. RESET BUFFER
    # ======================================================

    pdf.seek(0)

    # ======================================================
    # 9. DOWNLOAD
    # ======================================================

    return send_file(

        pdf,

        download_name=(
            f"SkinAI_Report_{report.report_id}.pdf"
        ),

        mimetype="application/pdf",

        as_attachment=True
    )


# ==========================================================
# SETTINGS
#
# /doctor/settings
# ==========================================================

@doctor.route(
    "/settings",
    methods=["GET", "POST"]
)
@login_required
def settings():

    # ======================================================
    # CHANGE PASSWORD
    # ======================================================

    if request.method == "POST":

        current_password = (
            request.form.get(
                "current_password",
                ""
            ).strip()
        )

        new_password = (
            request.form.get(
                "new_password",
                ""
            ).strip()
        )

        confirm_password = (
            request.form.get(
                "confirm_password",
                ""
            ).strip()
        )

        # --------------------------------------------------
        # Kiểm tra mật khẩu hiện tại
        # --------------------------------------------------

        if not current_password:

            flash(
                "Vui lòng nhập mật khẩu hiện tại.",
                "warning"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        if not check_password_hash(
            current_user.password_hash,
            current_password
        ):

            flash(
                "Mật khẩu hiện tại không chính xác.",
                "danger"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        # --------------------------------------------------
        # Kiểm tra mật khẩu mới
        # --------------------------------------------------

        if not new_password:

            flash(
                "Vui lòng nhập mật khẩu mới.",
                "warning"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        # --------------------------------------------------
        # Độ dài mật khẩu
        # --------------------------------------------------

        if len(new_password) < 6:

            flash(
                "Mật khẩu mới phải có ít nhất 6 ký tự.",
                "warning"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        # --------------------------------------------------
        # Xác nhận mật khẩu
        # --------------------------------------------------

        if new_password != confirm_password:

            flash(
                "Mật khẩu xác nhận không khớp.",
                "danger"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        # --------------------------------------------------
        # Không cho dùng lại mật khẩu cũ
        # --------------------------------------------------

        if check_password_hash(
            current_user.password_hash,
            new_password
        ):

            flash(
                "Mật khẩu mới phải khác mật khẩu hiện tại.",
                "warning"
            )

            return redirect(
                url_for(
                    "doctor.settings"
                )
            )

        # --------------------------------------------------
        # Tạo password hash mới
        # --------------------------------------------------

        current_user.password_hash = (
            generate_password_hash(
                new_password
            )
        )

        db.session.commit()

        flash(
            "Đổi mật khẩu thành công.",
            "success"
        )

        return redirect(
            url_for(
                "doctor.settings"
            )
        )

    # ======================================================
    # DOCTOR PROFILE
    # ======================================================

    doctor_profile = (
        current_user.doctor_profile
    )

    return render_template(
        "doctor/settings.html",
        doctor_profile=doctor_profile
    )


# ==========================================================
# REVIEW
# ==========================================================

@doctor.route(
    "/review/<int:image_id>",
    methods=["GET", "POST"]
)
@login_required
def review(image_id):

    lesion = (
        LesionImageRepository
        .get_by_id(
            image_id
        )
    )

    prediction = (
        AIRepository
        .get_prediction_by_image(
            image_id
        )
    )

    if prediction is None:

        flash(
            "Ảnh chưa được AI dự đoán.",
            "warning"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )

    form = DoctorReviewForm()

    if form.validate_on_submit():

        DoctorReportService.confirm(

            lesion.exam_id,

            current_user
            .doctor_profile
            .doctor_id,

            prediction.prediction_id,

            form

        )

        flash(
            "Đã xác nhận kết quả AI.",
            "success"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )

    return render_template(

        "doctor/review.html",

        lesion=lesion,

        prediction=prediction,

        form=form

    )

# ==========================================================
# ICD-10 LOOKUP
# ==========================================================

@doctor.route("/icd10")
@login_required
def icd10():

    q = request.args.get(
        "q",
        "",
        type=str
    ).strip()

    # Chưa tìm kiếm
    if not q:
        return render_template(
            "doctor/icd10.html",
            result=None,
            total=0,
            q=""
        )

    keyword = f"%{q}%"

    # ======================================================
    # TÌM ICD-10
    # ======================================================

    sql = text("""
        SELECT
            id,
            code,
            code_display,
            short_description_en,
            long_description_en,
            short_description_vi,
            long_description_vi
        FROM icd10
        WHERE
            code ILIKE :keyword
            OR code_display ILIKE :keyword
            OR short_description_en ILIKE :keyword
            OR long_description_en ILIKE :keyword
            OR short_description_vi ILIKE :keyword
            OR long_description_vi ILIKE :keyword
        ORDER BY
            CASE
                WHEN UPPER(code) = UPPER(:exact)
                    THEN 0

                WHEN UPPER(code_display) = UPPER(:exact)
                    THEN 1

                WHEN UPPER(code) LIKE UPPER(:prefix)
                    THEN 2

                WHEN LOWER(short_description_en)
                     LIKE LOWER(:prefix)
                    THEN 3

                WHEN LOWER(short_description_vi)
                     LIKE LOWER(:prefix)
                    THEN 4

                ELSE 5
            END,
            code_display ASC
        LIMIT 1
    """)

    result = db.session.execute(
        sql,
        {
            "keyword": keyword,
            "exact": q,
            "prefix": f"{q}%"
        }
    )

    row = result.mappings().first()

    # ======================================================
    # ĐẾM KẾT QUẢ
    # ======================================================

    count_sql = text("""
        SELECT COUNT(*)
        FROM icd10
        WHERE
            code ILIKE :keyword
            OR code_display ILIKE :keyword
            OR short_description_en ILIKE :keyword
            OR long_description_en ILIKE :keyword
            OR short_description_vi ILIKE :keyword
            OR long_description_vi ILIKE :keyword
    """)

    count_result = db.session.execute(
        count_sql,
        {
            "keyword": keyword
        }
    )

    total = count_result.scalar() or 0

    # ======================================================
    # CHUYỂN DATA
    # ======================================================

    result_data = None

    if row:

        name_vi = (
            row["short_description_vi"]
            or get_vietnamese_name(
                row["code"],
                row["short_description_en"]
            )
        )

        description_vi = (
            row["long_description_vi"]
            or get_vietnamese_description(
                row["code"],
                row["long_description_en"]
            )
        )

        if not description_vi:
            description_vi = (
                name_vi
                or "Chưa có mô tả tiếng Việt."
            )

        result_data = {

            "id": row["id"],

            "code": row["code"],

            "code_display": row["code_display"],

            "name_vi": name_vi,

            "name_en": (
                row["short_description_en"]
                or "Chưa có thông tin"
            ),

            "description_vi": description_vi,

            "description_en": (
                row["long_description_en"]
                or "Chưa có thông tin"
            )
        }

    return render_template(
        "doctor/icd10.html",
        result=result_data,
        total=total,
        q=q
    )


# ==========================================================
# EXPORT PDF BY IMAGE
#
# /doctor/export-pdf/123
# ==========================================================

@doctor.route(
    "/export-pdf/<int:image_id>"
)
@login_required
def export_pdf(image_id):

    # ======================================================
    # 1. LESION
    # ======================================================

    lesion = (
        LesionImageRepository
        .get_by_id(
            image_id
        )
    )

    if lesion is None:

        flash(
            "Không tìm thấy ảnh.",
            "danger"
        )

        return redirect(
            url_for(
                "doctor.lesions"
            )
        )

    # ======================================================
    # 2. PREDICTION
    # ======================================================

    prediction = (
        AIRepository
        .get_prediction_by_image(
            image_id
        )
    )

    if prediction is None:

        flash(
            "Ảnh chưa được AI dự đoán.",
            "warning"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )

    # ======================================================
    # 3. AI RESULTS
    # ======================================================

    results = (
        AIRepository
        .get_prediction_details(
            prediction.prediction_id
        )
    )

    heatmap = (
        AIRepository
        .get_heatmap(
            prediction.prediction_id
        )
    )

    # ======================================================
    # 4. REPORT
    # ======================================================

    report = (
        DoctorReportRepository
        .get_by_image(
            image_id
        )
    )

    # ======================================================
    # 5. EXAM
    # ======================================================

    exam = lesion.examination

    if exam is None:

        flash(
            "Không tìm thấy ca khám.",
            "danger"
        )

        return redirect(
            url_for(
                "lesion.detail",
                image_id=image_id
            )
        )

    # ======================================================
    # 6. PATIENT
    # ======================================================

    patient = exam.patient

    # ======================================================
    # 7. DOCTOR
    # ======================================================

    doctor = (

        report.doctor

        if report

        else exam.doctor

    )

    # ======================================================
    # 8. DEBUG
    # ======================================================

    print(
        "=========================================="
    )

    print(
        "EXPORT BY IMAGE:",
        image_id
    )

    print(
        "IMAGE PATH:",
        lesion.image_path
    )

    print(
        "PREDICTION:",
        prediction
    )

    print(
        "RESULTS:",
        results
    )

    print(
        "HEATMAP:",
        heatmap
    )

    print(
        "=========================================="
    )

    # ======================================================
    # 9. GENERATE PDF
    # ======================================================

    pdf = PDFService.generate_pdf({

        "patient": patient,

        "doctor": doctor,

        "exam": exam,

        "lesion": lesion,

        "lesion_image": lesion.image_path,

        "prediction": prediction,

        "results": results,

        "report": report,

        "heatmap": heatmap

    })

    # ======================================================
    # 10. RESET BUFFER
    # ======================================================

    pdf.seek(0)

    # ======================================================
    # 11. DOWNLOAD
    # ======================================================

    return send_file(

        pdf,

        download_name=(
            f"SkinAI_Report_{image_id}.pdf"
        ),

        mimetype="application/pdf",

        as_attachment=True
    )

