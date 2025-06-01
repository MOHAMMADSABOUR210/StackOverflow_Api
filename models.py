from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///questions.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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

class Tags(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tags = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    owner = db.Column(db.String, nullable=False)
    is_answered = db.Column(db.Boolean)
    view_count = db.Column(db.Integer)
    answer_count = db.Column(db.Integer)
    score = db.Column(db.Integer)

class SearchQuestion(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    link = db.Column(db.String, nullable=False)
    is_answered = db.Column(db.Boolean)
