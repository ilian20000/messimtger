import flask
from flask import redirect, url_for
from functools import wraps

import database.models
from database.database import db, init_database
from database.populate_database import populate_database

import session_manager


app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'verysecretkey'

db.init_app(app)
with app.test_request_context():
    init_database()
    populate_database()


@app.route("/")
def index():
    return redirect(url_for("home"))

@app.route('/home')
def home():
    return flask.render_template("home.html.jinja2")

@app.route('/contact')
def contact():
    return flask.render_template("contact.html.jinja2")

@app.route('/login')
def login():
    return flask.render_template("login.html.jinja2")

@app.route('/register')
def register():
    return flask.render_template("register.html.jinja2")


def is_connected(f):
    @wraps(f)
    def decorator_f(*args, **kwargs):
        if 'username' in flask.session:
            return f(*args, **kwargs)
        else:
            return redirect(url_for("login"))
    return decorator_f


@app.route("/dashboard")
@is_connected
def dashboard():
    return flask.render_template("dashboard.html.jinja2")



@app.route('/login', methods=['GET', 'POST'])
def login_callback():
    donnees = flask.request.form
    username = donnees.get("identifier")
    password = donnees.get("password")

    login_status = session_manager.login_check(username, password, app.secret_key)
    login_error_msg = "Mot de passe ou nom d'utilisateur incorrect"

    if login_status and username:
        flask.session["username"]=username
        return flask.redirect(flask.url_for("dashboard"))
    return flask.render_template("login.html.jinja2", login_error_msg=login_error_msg)

@app.route('/dashboard', methods=['GET', 'POST'])
def logout_callback():
    print('Session clearing...')
    flask.session.clear()
    print('Session cleared')
    return flask.redirect(flask.url_for("home"))

@app.route('/register', methods=['GET', 'POST'])
def register_callback():
    donnees = flask.request.form
    username = donnees.get("username")
    email = donnees.get("email")
    password = donnees.get("password")
    password_confirm = donnees.get("password_confirm")

    register_status, register_error_msg = session_manager.register_check(username, email, password, password_confirm)

    if not register_status:
        return flask.render_template("register.html.jinja2", register_error_msg=register_error_msg)

    session_manager.register_new_user(username, email, password)
    db.session["username"] = username
    return flask.redirect(flask.url_for("dashboard"))


if __name__ == "__main__":
    app.run(debug=True)


