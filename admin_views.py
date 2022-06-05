from flask import render_template, flash, redirect, Blueprint, request, url_for
from models import Quiz, Question, Answer, db
from flask_login import login_required, current_user
my_view = Blueprint('my_view', __name__)

@my_view.route("/")
def home():
    return render_template("index.html")

@my_view.route("/view_quiz")
def view_quiz():
    quizzes = Quiz.query.all()
    return render_template("view_quiz.html", quizzes=quizzes)

@login_required
@my_view.route("/add_quiz", methods=["GET", "POST"])
def add_quiz():
    if "Admin" in current_user.roles:
        if request.method == "POST":
            # another bit of logic to determine add from remove
            quiz_name = request.form["quiz_name"]
            new_quiz = Quiz(name=quiz_name)
            db.session.add(new_quiz)
            db.session.commit()
            return render_template("admin/add_questions.html", added_prev=True, quiz_name=quiz_name)
        return render_template("admin/add_quiz.html")        
    else:
        return redirect(url_for("login_views.dashboard"))


@my_view.route("/add_questions/<quiz_name>", methods=["GET", "POST"])
@my_view.route("/add_questions", methods=["GET", "POST"])
def add_questions(quiz_name):
    if "Admin" in current_user.roles:
        if request.method == "POST":
            quiz_name = request.form["quiz_name"]
            print(f'this is the quiz name {quiz_name}')
            quiz_obj = Quiz.query.filter_by(name=quiz_name).first()
            print(f"this is the obj {quiz_obj}")
            if quiz_name:
                question_name = request.form["question_name"]
                new_answer_1 = request.form["answer_name1"]
                new_answer_2 = request.form["answer_name2"]
                new_answer_3 = request.form["answer_name3"]
                new_answer_4 = request.form["answer_name4"]
                option = request.form['correct_answer']
                new_question = Question(name=question_name, quiz=quiz_obj)
                db.session.add(new_question)
                if option == "1":
                    set_answer_1 = Answer(name=new_answer_1,correct=True)
                    set_answer_2 = Answer(name=new_answer_2,correct=False)
                    set_answer_3 = Answer(name=new_answer_3,correct=False)
                    set_answer_4 = Answer(name=new_answer_4,correct=False)
                elif option == "2":
                    set_answer_1 = Answer(name=new_answer_1,correct=False)
                    set_answer_2 = Answer(name=new_answer_2,correct=True)
                    set_answer_3 = Answer(name=new_answer_3,correct=False)
                    set_answer_4 = Answer(name=new_answer_4,correct=False)
                elif option == "3":
                    set_answer_1 = Answer(name=new_answer_1,correct=False)
                    set_answer_2 = Answer(name=new_answer_2,correct=False)
                    set_answer_3 = Answer(name=new_answer_3,correct=True)
                    set_answer_4 = Answer(name=new_answer_4,correct=False)
                elif option == "4":
                    set_answer_1 = Answer(name=new_answer_1,correct=False)
                    set_answer_2 = Answer(name=new_answer_2,correct=False)
                    set_answer_3 = Answer(name=new_answer_3,correct=False)
                    set_answer_4 = Answer(name=new_answer_4,correct=True)
                
                new_question.answers=[set_answer_1, set_answer_2, set_answer_3, set_answer_4]
                db.session.add(new_question)

                db.session.commit()
                return render_template("admin/add_questions.html", added_prev=True, quiz_name=quiz_name)
        else:
            # quiz_name = Quiz.query.filter_by(name=entry_name).first()
            return render_template("admin/add_questions.html", quiz_name=quiz_name)
    else:
        return redirect(url_for("login_views.dashboard"))

@my_view.route("/show_quiz", methods=["GET", "POST"])
def show_quiz():
    if "Admin" in current_user.roles:
        quizzes = Quiz.query.all()
        return render_template("admin/show_quiz.html", quizzes=quizzes)
    else:
        return redirect(url_for("login_views.dashboard"))

@my_view.route("/delete/<entry_name>", methods=["GET", "POST"])
def delete(entry_name):
    if "Admin" in current_user.roles:
        quizzes = Quiz.query.all()
        quiz_list = Quiz.query.filter_by(name=entry_name).first()
        db.session.delete(quiz_list)
        db.session.commit()
        if not Quiz.query.filter_by(name=entry_name).first():
            quizzes = Quiz.query.all()
            return render_template("admin/show_quiz.html", quizzes=quizzes)
        return render_template("admin/show_quiz.html", quizzes=quizzes)
    else:
        return redirect(url_for("login_views.dashboard"))

@my_view.route("/update/<entry_name>", methods=["GET", "POST"])
def update(entry_name):
    if "Admin" in current_user.roles:
        quizzes = Quiz.query.all()
        quiz_obj = Quiz.query.filter_by(name=entry_name).first()
        print(quiz_obj.name)
        # Update current questions
        if request.method == "POST":
            print("Got HERE!111")
            quiz_obj.name = request.form["quiz_name"]
            question_list = []
            answer_list = []
            for x in range(len(quiz_obj.questions)):
                question_list.append(request.form[str(quiz_obj.questions[x].name)])
                answer_list.append([])
                for i in range(len(quiz_obj.questions[x].answers)):
                    print("Got here 1")
                    x_answer = request.form[quiz_obj.questions[x].answers[i].name]
                    answer_list[x].append(x_answer)
                    
                print(answer_list)
            for x in range(len(quiz_obj.questions)):
                print("Got here 2")
                quiz_obj.questions[x].name = question_list[x]
                for i in range(len(quiz_obj.questions[x].answers)):
                    quiz_obj.questions[x].answers[i].name = answer_list[x][i]
                
            
            db.session.commit()
        else:
            print("DESTINGATION 2")
        
        if not Quiz.query.filter_by(name=entry_name).first():
            return render_template("admin/show_quiz.html", quizzes=quizzes, quiz_obj=quiz_obj, quiz_name=entry_name)
        return render_template("admin/update_quiz.html", quizzes=quizzes, quiz_obj=quiz_obj, quiz_name=entry_name)
    else:
        return redirect(url_for("login_views.dashboard"))

from wtforms import StringField
from wtforms.validators import DataRequired

class SearchForm(Form):
    search = StringField('search', [DataRequired()])
    submit = SubmitField('Search',
                        render_kw={'class': 'btn btn-success btn-block'})


@app.route('/search', methods=['POST', 'GET'])
@login_required
def search():
    form = SearchForm()
    if not form.validate_on_submit():
        return redirect(url_for('index'))
    return redirect((url_for('search_results', query=form.search.data)))

@app.route('/search_results/<query>')
@login_required
def search_results(query):
    results = Quiz.query.filter_by(name=query)
    return render_template('search_results.html', query=query, results=results)
