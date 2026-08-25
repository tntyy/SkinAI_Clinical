from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.user import User
from app.models.doctor_profile import DoctorProfile
from app.database.db import db
from flask_login import login_user, logout_user
from app.auth import auth
from flask_login import current_user

@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form.get("username")
        password = request.form.get("password")

        user = User.query.filter_by(
            username=username
        ).first()

        if user and check_password_hash(
                user.password_hash,
                password
        ):

            login_user(user)

            flash(
                "Đăng nhập thành công!",
                "success"
            )

            if user.role == "doctor":
                return redirect(
                    url_for("doctor.dashboard")
                )

            else:
                flash(
                    "Tài khoản không có quyền truy cập.",
                    "danger"
                )

                logout_user()

                return redirect(
                    url_for("auth.login")
                )

        flash(
            "Sai tài khoản hoặc mật khẩu!",
            "danger"
        )

    return render_template("auth/login.html")


@auth.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        fullname = request.form.get("fullname", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        hospital = request.form.get("hospital", "").strip()
        department = request.form.get("department", "").strip()

        # --------------------------------------------------
        # Kiểm tra dữ liệu bắt buộc
        # --------------------------------------------------

        if not username or not password or not fullname:

            flash(
                "Vui lòng nhập đầy đủ tên đăng nhập, mật khẩu và họ tên.",
                "warning"
            )

            return redirect(url_for("auth.register"))

        if len(password) < 6:

            flash(
                "Mật khẩu phải có ít nhất 6 ký tự.",
                "warning"
            )

            return redirect(url_for("auth.register"))

        if password != confirm_password:

            flash(
                "Mật khẩu xác nhận không khớp.",
                "danger"
            )

            return redirect(url_for("auth.register"))

        # --------------------------------------------------
        # Kiểm tra trùng tên đăng nhập
        # --------------------------------------------------

        existing_user = User.query.filter_by(
            username=username
        ).first()

        if existing_user:

            flash(
                "Tên đăng nhập đã tồn tại, vui lòng chọn tên khác.",
                "danger"
            )

            return redirect(url_for("auth.register"))

        # --------------------------------------------------
        # Tạo tài khoản (mặc định vai trò doctor)
        # --------------------------------------------------

        new_user = User(
            username=username,
            password_hash=generate_password_hash(password),
            role="doctor",
            is_active=True
        )

        db.session.add(new_user)
        db.session.flush()

        new_profile = DoctorProfile(
            user_id=new_user.user_id,
            fullname=fullname,
            email=email or None,
            phone=phone or None,
            hospital=hospital or None,
            department=department or None
        )

        db.session.add(new_profile)
        db.session.commit()

        flash(
            "Đăng ký tài khoản bác sĩ thành công! Vui lòng đăng nhập.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth.route("/logout")
def logout():

    logout_user()

    flash(
        "Đăng xuất thành công.",
        "success"
    )

    return redirect(
        url_for("auth.login")
    )