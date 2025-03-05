from datetime import timezone
from flask_login import UserMixin
from sqlalchemy.sql import func
from . import db

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    user_name = db.Column(db.String(150), unique=True, nullable=False)
    notes = db.relationship("Note", backref="user", lazy=True)
    is_blocked = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, email, password, user_name, is_blocked=False, is_admin=False):
        self.email = email
        self.password = password
        self.user_name = user_name
        self.is_blocked = is_blocked
        self.is_admin = is_admin