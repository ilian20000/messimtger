import flask
import os

from flask import redirect, url_for

import database.models
from database.database import db, init_database
from database.populate_database import populate_database

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

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

@app.route('/login', methods=['GET', 'POST'])
def login_callback():
    donnees = flask.request.form
    email = donnees.get("email")
    password = donnees.get("password")

    print("MUST CHECK LOGIN", email, password)
    return flask.redirect(flask.url_for("home"))


@app.route('/register')
def register():
    return flask.render_template("register.html.jinja2")


@app.route('/register', methods=['GET', 'POST'])
def register_callback():
    donnees = flask.request.form
    email = donnees.get("email")
    username = donnees.get("username")
    password = donnees.get("password")
    password_confirm = donnees.get("password_confirm")

    print("MUST TRIGGER REGISTER", email, username, password, password_confirm)
    return flask.redirect(flask.url_for("home"))


@app.route("/dashboard")
def dashboard():
    engineer = database.models.Engineer.query.get(3310)
    print(engineer)
    return flask.render_template("dashboard.html.jinja2", engineer=engineer)


if __name__ == "__main__":
    app.run(debug=True)


