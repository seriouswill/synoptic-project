from flask import render_template, flash, redirect, Blueprint, request, url_for
from models import Quiz, Question, Answer, db
from login_views import QuizScore, User
from flask_login import current_user

user_view = Blueprint('user_view', __name__)

@user_view.route("/quiz_portal")
def quiz_portal():
    quiz_total_list = Quiz.query.all()
    return render_template("user/quiz_portal.html", quiz_total_list=quiz_total_list)

@user_view.route("/play_quiz/<quiz_title>", methods=["GET", "POST"])
def play_quiz(quiz_title):
    quiz_title = Quiz.query.filter_by(name=quiz_title).first()
    result = 0
    total = len(quiz_title.questions)
    if request.method == "POST":
        for question in quiz_title.questions:
            for answer in question.answers:
                checkbox_bool = request.form.get(f"answer-checkbox-{answer.name}")
                print(checkbox_bool)
                if checkbox_bool == "on" and answer.correct == True:
                    result += 1
                    print(result)
        new_quiz_score = QuizScore(quiz_name=quiz_title.name, quiz_max_score=total, quiz_score=result)
        current_user.quiz_scores.append(new_quiz_score)
        db.session.commit()
        return render_template("user/quiz_results.html", result=result, total=total, quiz_title=quiz_title)
    return render_template("user/play_quiz.html", quiz_title=quiz_title, total=total)


@user_view.route("/quiz_submit", methods=["GET", "POST"])
def quiz_submit():
    return render_template("user/quiz_results.html")