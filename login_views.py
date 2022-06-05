from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, redirect, url_for, Blueprint, request
from flask_wtf import FlaskForm 
login_views = Blueprint('login_views', __name__)
from flask_security import Security, SQLAlchemyUserDatastore, RoleMixin
from flask_security.utils import hash_password
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
from flask_security.forms import LoginForm



from models import db, app
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login_views.login"


roles_users = db.Table('roles_users', 
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    active = db.Column(db.Boolean, default=True)
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy="dynamic"))
    quiz_scores = db.relationship('QuizScore', cascade="all, delete, delete-orphan", backref="user")

class QuizScore(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    quiz_name = db.Column(db.String(300))
    quiz_max_score = db.Column(db.Integer)
    quiz_score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40))
    description = db.Column(db.String(255))

# ! Need to check this custom form
class CustomLoginForm(LoginForm):
    username = StringField('username')

@login_views.route('/login_custom',  methods=["GET", "POST"])
def login_custom():
    return render_template("security/login_custom.html")

# @login_views.route('/login',  methods=["GET", "POST"])
# def login():
#     form = LoginForm()

#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user:
#             if check_password_hash(user.password, form.password.data):
#                 login_user(user, form.remember.data)
#                 return redirect(url_for('login_views.dashboard'))
#     else:
#         return render_template("login.html", form=form, invalid=False)
#     return render_template("login.html", form=form, invalid=True)

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=CustomLoginForm)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@login_views.route("/register", methods=["GET", "POST"])
def register():
    default_role = [Role.query.filter_by(name="User").first()]
    if request.method == "POST":
        user_datastore.create_user(username=request.form.get('username'),
            email=request.form.get('email'),
            password=hash_password(request.form.get('password')),
            roles=default_role)
        db.session.commit()
    return render_template("register.html")


# @login_views.route('/signup', methods=["GET", "POST"])
# def signup():
#     form = RegisterForm()
#     default_role = [Role.query.filter_by(name="User").first()]
#     if form.validate_on_submit():
#         hashed_password = generate_password_hash(form.password.data, method="sha256")
#         new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, roles=default_role)
#         db.session.add(new_user)
#         db.session.commit()
#     return render_template("signup.html", form=form)



@login_views.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("index.html")


@login_views.route('/dashboard')
@login_required
def dashboard():

    quiz_score_title_list = QuizScore.query.filter_by(user_id=current_user.id).all()
    return render_template("dashboard.html", name=current_user.username, quiz_score_title_list=quiz_score_title_list)
