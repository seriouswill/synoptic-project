# In this section I will be using the design class recipe method to test-drive my classes into existence.

## Step One - User Stories

### As a Client
### I want a web based quiz application
### In order to field quizzes out to Users

### As a Client
### I want to be able to view, edit and delete the quizzes, and questions
### In order to have a maintable and customisable quiz app

### As a User
### In order to test my programming knowledge
### I would like to view and answer quiz questions

## Step Two - Design Signiture Classes

    python """
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
    """

## Step Three - Create Examples as Tests

``` python

# test suite one

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
```

## Behaviour Implementation

### see "./test_db_models.py"