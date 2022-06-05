
# ! using pytest in order to test, run pytest

from models import Quiz, Question, Answer, db

# ? integration tests

def test_quiz_model():
    test_quiz = Quiz(name="test1")
    db.session.add(test_quiz)
    test_question = Question(name="question test one", quiz=test_quiz)
    test_answer_1 = Answer(name="answer one",correct=True)
    test_answer_2 = Answer(name="answer two",correct=False)
    test_answer_3 = Answer(name="answer three",correct=False)
    test_answer_4 = Answer(name="answer four",correct=False)
    test_question.answers=[test_answer_1, test_answer_2, test_answer_3, test_answer_4]
    db.session.add(test_question)
    db.session.commit()

    # now to query and test

    assert test_quiz.name == "test1"
    assert test_question in test_quiz.questions
    assert test_quiz.questions[0].name == "question test one"
    assert test_answer_1 in test_quiz.questions[0].answers
    assert test_quiz.questions[0].answers[0].name == "answer one"
    assert test_quiz.questions[0].answers[2].name == "answer three"

# ! Tests successful 

# ? integration testing User Role and QuizScore

from login_views import user_datastore, User, Role, Answer
import flask_security

def test_User_Role_QuizScore_model():
    test_user = user_datastore.create_user(username="test_username",
            email="test_email@test.com",
            password="test_password",
            roles="test")
    db.session.commit()

    test_query = User.query.filter_by(username="test_username").first()
    assert test_query.email == "test_email@test.com"
    assert test_query.password == "test_password"
    assert test_query.roles == "test"