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

## Behaviour Implementation

### see "./test_db_models.py"