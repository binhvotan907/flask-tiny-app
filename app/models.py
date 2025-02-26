from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    """Bảng lưu thông tin người dùng"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    tasks = db.relationship('Task', backref='owner', lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"

class Post(db.Model):
    """Bảng lưu bài viết của người dùng"""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Post {self.title}>"

class Task(db.Model):
    """Bảng lưu danh sách nhiệm vụ của người dùng"""
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Task {self.description} - {'Done' if self.completed else 'Pending'}>"
