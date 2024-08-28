import datetime
import os

import flask
from flask import redirect, url_for
from functools import wraps
from werkzeug.utils import secure_filename

from database.database import db, init_database
from database.models import User, Conversation, Message
from database.populate_database import populate_database

import session_manager

app = flask.Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['UPLOAD_FOLDER'] = os.path.join("database", "image_database")
app.secret_key = 'verysecretkey'

db.init_app(app)
with app.test_request_context():
    init_database()
    populate_database()


@app.route("/")
def index():
    return redirect(url_for("home"))

@app.route('/home/')
def home():
    return flask.render_template("home.html.jinja2")

@app.route('/contact/')
def contact():
    return flask.render_template("contact.html.jinja2")

@app.route('/login/')
def login():
    return flask.render_template("login.html.jinja2")

@app.route('/register/')
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


@app.route("/dashboard/")
@is_connected
def dashboard():
    group_conversations = Conversation.query.filter_by(is_private=False)
    private_conversations = Conversation.query.filter_by(is_private=True)
    return flask.render_template("dashboard.html.jinja2",
                                 private_conversations=private_conversations,
                                 group_conversations=group_conversations)


@app.route("/dashboard/<int:conversation_id>/")
@is_connected
def dashboard_select(conversation_id):
    active_conversation = Conversation.query.filter_by(conversation_id=conversation_id).first()
    group_conversations = Conversation.query.filter_by(is_private=False)
    private_conversations = Conversation.query.filter_by(is_private=True)

    if active_conversation:
        return flask.render_template("dashboard.html.jinja2",
                                     private_conversations=private_conversations,
                                     group_conversations=group_conversations,
                                     active_conversation=active_conversation)
    print("No conversation selected, redirect to empty page");
    return redirect(url_for("dashboard"))


@app.route('/login/', methods=['GET', 'POST'])
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

# @app.route('/dashboard/')
# @app.route('/dashboard/<int:conversation_id>/')
@app.route('/*')
def logout_callback():
    print('Session clearing...')
    flask.session.clear()
    print('Session cleared')
    return flask.redirect(flask.url_for("home"))


@app.route('/register/', methods=['GET', 'POST'])
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
    flask.session["username"] = username
    return flask.redirect(flask.url_for("dashboard"))


@app.route('/dashboard/<int:conversation_id>/', methods=['GET', 'POST'])
@is_connected
def send_message_callback(conversation_id):
    print("TAMERE")
    donnees = flask.request.form
    new_message_text = donnees.get("new_message_text")
    author_username = flask.session["username"]
    image_upload = flask.request.files["image_input"]
    if image_upload.filename == '':
        flask.flash('No upload file')
        session_manager.send_new_message(conversation_id, author_username, new_message_text)
        return flask.redirect(flask.url_for("dashboard_select", conversation_id=conversation_id))

    image_new_name = secure_filename(image_upload.filename)
    image_upload.save(os.path.join(app.config['UPLOAD_FOLDER'], image_new_name))
    flask.flash('File successfully uploaded ' + image_new_name)

    session_manager.send_new_message(conversation_id, author_username, new_message_text, image_new_name)

    return flask.redirect(flask.url_for("dashboard_select", conversation_id=conversation_id))


# @app.route('/dashboard/<int:conversation_id>/', methods=['GET', 'POST'])
@app.route('/uploads/<path:image_filename>/', methods=['GET', 'POST'])
@is_connected
def display_image_link(image_filename):
    print("TAMERE")
    # image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
    print(str(image_filename))
    return flask.send_from_directory(app.config['UPLOAD_FOLDER'], image_filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)


