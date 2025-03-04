from math import e
from re import template
from flask import Blueprint, render_template, request, flash, session
from flask.helpers import url_for
from sqlalchemy.sql.expression import false
from werkzeug.utils import redirect
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import timedelta
from todolist import views
from .models import User, Note

from . import db

user = Blueprint("user", __name__)


@user.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                session.permanent = True
                login_user(user, remember=True)
                flash("Đăng nhập thành công!", category="success")
                return redirect(url_for("views.home"))
            else:
                flash("Sai mật khẩu, vui lòng kiểm tra lại!", category="error")
        else:
            flash("Người dùng không tồn tại!", category="error")
    return render_template("login.html", user=current_user)


@user.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        user_name = request.form.get("user_name")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")

        user = User.query.filter_by(email=email).first()
        # validate user
        if user:
            flash("Người dùng đã tồn tại!", category="error")
        elif len(email) < 4:
            flash("Email phải lớn hơn 3 ký tự.", category="error")
        elif len(password) < 7:
            flash("Email phải lớn hơn 7 ký tự.", category="error")
        elif password != confirm_password:
            flash("Mật khẩu không khớp!", category="error")
        else:
            password = generate_password_hash(password, method="pbkdf2:sha256") 

            new_user = User(email=email, password=password, user_name=user_name)
            try:
                db.session.add(new_user)
                db.session.commit()
                flash("Đăng kí người dùng thành công!", category="success")
                login_user(new_user, remember=True)  # Sửa user thành new_user
                return redirect(url_for("views.home"))
            except Exception as e:
                 flash(f"Lỗi khi tạo người dùng: {str(e)}", category="error")

    return render_template("signup.html", user=current_user)


@user.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("user.login"))
