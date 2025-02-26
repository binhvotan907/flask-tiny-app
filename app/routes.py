from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, Post, Task
from app.forms import RegistrationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

# Tạo Blueprint cho routes
bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash("Đăng ký thành công! Vui lòng đăng nhập.", "success")
        return redirect(url_for('main.login'))
    return render_template('register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user)
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('main.home'))
        else:
            flash("Sai email hoặc mật khẩu.", "danger")
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Bạn đã đăng xuất.", "info")
    return redirect(url_for('main.index'))

@bp.route('/home')
@login_required
def home():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)

@bp.route('/tasks')
@login_required
def tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=tasks)

@bp.route('/add_task', methods=['POST'])
@login_required
def add_task():
    description = request.form.get('description')
    if description:
        task = Task(description=description, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        flash("Nhiệm vụ đã được thêm!", "success")
    return redirect(url_for('main.tasks'))

@bp.route('/complete_task/<int:task_id>')
@login_required
def complete_task(task_id):
    task = Task.query.get_or_404(task_id)
    if task.user_id == current_user.id:
        task.completed = True
        db.session.commit()
        flash("Nhiệm vụ đã hoàn thành!", "success")
    return redirect(url_for('main.tasks'))
