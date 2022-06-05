from flask import Flask, render_template #! here we put our flask imports
from flask_bootstrap import Bootstrap

from models import app, Quiz, Answer, Question, create_db_models
from admin import admin

Bootstrap(app)
from admin_views import my_view
app.register_blueprint(my_view)

from login_views import create_db_users ,login_views, User, Role, QuizScore, roles_users
app.register_blueprint(login_views)

from user_views import user_view
app.register_blueprint(user_view)

def create_db():
    create_db_models()
    create_db_users()

if __name__ == "__main__":
    app.run(debug=True, port=8000)


#! In order to instantiate the db you may need to uncomment this function and run db.create_all()
# create_db()