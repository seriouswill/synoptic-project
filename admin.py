from flask_admin import Admin, AdminIndexView
from models import app, db, Quiz, Question, Answer
from login_views import User, roles_users, Role
from flask import url_for, redirect

from flask_login import current_user
from flask_admin.contrib.sqla import ModelView

app.config['SECRET_KEY'] = "thisisasecret"

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

class MyModelView(ModelView):
    def is_accessible(self):
        if "Admin" in current_user.roles: return True

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for("login_views.login"))

# Overwritten the ModelView class to hide information for non-admin

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if "Admin" in current_user.roles: return True
        

# Overwritten the AdminIndexView in roder to secure admin priviledges

admin = Admin(app, index_view=MyAdminIndexView())

admin.add_view(MyModelView(Quiz, db.session))
admin.add_view(MyModelView(Question, db.session))
admin.add_view(MyModelView(Answer, db.session))
admin.add_view(MyModelView(User, db.session))
admin.add_view(MyModelView(Role, db.session))