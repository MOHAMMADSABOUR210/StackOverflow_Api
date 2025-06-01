from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    tags = db.Column(db.String)
    is_answered = db.Column(db.Boolean)
    score = db.Column(db.Integer)
    creation_date = db.Column(db.Integer)
    body = db.Column(db.Text)
