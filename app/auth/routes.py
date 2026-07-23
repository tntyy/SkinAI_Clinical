from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash
from app.models.user import User
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

            return redirect(
                url_for("doctor.dashboard")
            )

        flash(
            "Sai tài khoản hoặc mật khẩu!",
            "danger"
        )

    return render_template("auth/login.html")


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