from flask_login import UserMixin
from initial import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    is_teacher=db.Column(db.Boolean, default=False)
    std=db.Column(db.Integer())

class Questions(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    question=db.Column(db.String(1000))
    description=db.Column(db.String(100000))
    author=db.Column(db.String(1000))
    std=db.Column(db.Integer())
    answer=db.Column(db.String(100000))
    subject=db.Column(db.String(100))