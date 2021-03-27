from flask_login import UserMixin
from initial import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    std=db.Column(db.Integer())
    # questions=db.Column(db.String(100000), default=None)

class Questions(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    question=db.Column(db.String(1000))
    description=db.Column(db.String(100000))
    author=db.Column(db.String(1000))
    std=db.Column(db.Integer())
    answer=db.Column(db.String(100000))