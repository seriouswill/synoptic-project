from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "SuperSecret_keyyysysy"
if 'SECURITY_PASSWORD_SALT' not in app.config:
    app.config['SECURITY_PASSWORD_SALT'] = app.config['SECRET_KEY']
db = SQLAlchemy(app)

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(30))
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    questions = db.relationship('Question', cascade="all, delete, delete-orphan", backref="quiz")

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(300))
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)

    answers = db.relationship('Answer', cascade="all, delete, delete-orphan", backref="question")

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), nullable=False)
    correct = db.Column(db.Boolean, default=False, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

def create_db_models():
    db.create_all()