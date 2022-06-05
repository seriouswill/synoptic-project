from flask import Flask, render_template #! here we put our flask imports
from flask_bootstrap import Bootstrap

from models import app, db, Quiz, Answer, Question
from admin import admin

Bootstrap(app)
from admin_views import my_view
app.register_blueprint(my_view)

from login_views import login_views, User, Role, QuizScore, roles_users
app.register_blueprint(login_views)

from user_views import user_view
app.register_blueprint(user_view)

def create_db():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=8000)
