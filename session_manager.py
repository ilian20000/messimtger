from database.database import db

from database.models import User, Conversation, Message

from datetime import datetime
import re


USERNAME_MAX_LENGTH = 16
EMAIL_MAX_LENGTH = 64
PASSWORD_MAX_LENGTH = 64
PASSWORD_MIN_LENGTH = 6

UPLOAD_FOLDER = 'uploads/'  # Directory where uploaded images will be stored
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def register_check(username, email, password, password_confirm, secret_key):
    register_status = True
    register_error_msg = ""

    # special_caracters_list = r"-_!?/';,:#&+=%*"
    special_caracters_list = r"\"!#$%&'()*+,./:;<=>?@[\]^_`{|}~ -"

    regex_special_caracter = re.compile(r".*[" + special_caracters_list + "].*")
    regex_letter_lowercase = re.compile(r"[a-z]")
    regex_letter_uppercase = re.compile(r"[A-Z]]")
    regex_number = re.compile(r"[0-9]]")

    contains_special_caracter = re.match(regex_special_caracter, password)
    contains_letter_lowercase = re.match(regex_letter_lowercase, password)
    contains_letter_uppercase = re.match(regex_letter_uppercase, password)
    contains_number = re.match(regex_number, password)

    if len(username) > USERNAME_MAX_LENGTH:
        register_error_msg = "Nom d'utilisateur trop long (max {} caractères)".format(USERNAME_MAX_LENGTH)
        register_status = False

    # more complex password for later
    # elif not re.match(regex_contains_special_caracter, password):
    #     register_error_msg = "Mot de passe doit contenir un caractère spécial ({})".format(special_caracters_list)
    #     register_status = False

    elif (not contains_number) or (not contains_letter_uppercase and not contains_letter_lowercase):
        register_error_msg = "Mot de passe doit contenir au moins un nombre et une lettre"
        register_status = False

    elif User.query.filter_by(username=username).first():
        register_error_msg = "Ce pseudonyme est déjà associé à un compte existant"
        register_status = False

    elif User.query.filter_by(email=email).first():
        register_error_msg = "Cet adresse email est déjà associée à un compte existant"
        register_status = False

    elif len(email)>EMAIL_MAX_LENGTH:
        register_error_msg = "Email trop long (max {} caractères)".format(EMAIL_MAX_LENGTH)
        register_status = False

    elif len(password)>PASSWORD_MAX_LENGTH:
        register_error_msg = "Mot de passe trop long (max {} caractères)".format(PASSWORD_MAX_LENGTH)
        register_status = False

    elif len(password)<PASSWORD_MIN_LENGTH:
        register_error_msg = "Mot de passe trop court (min {} caractères)".format(PASSWORD_MIN_LENGTH)
        register_status = False

    elif password != password_confirm:
        register_error_msg = "Les deux mots de passe ne correspondent pas"
        register_status = False

    return register_status, register_error_msg


def register_new_user(email, username, password, secret_key):
    new_user = User(username=username, email=email, password=password)
    db.session.add(new_user)
    db.session.commit()


def login_check(identifier, password, secret_key):
    user_with_username = User.query.filter_by(username=identifier).first()
    user_with_email = User.query.filter_by(username=identifier).first()
    user_password = ""

    print("all users : ", User.query.all())
    print("login check username", user_with_username)
    print("login check email", user_with_email)

    if not user_with_username and not user_with_email:
        print("User with id {} does not exist".format(identifier))
        return False

    if user_with_username:
        user_password = user_with_username.password

    if user_with_email:
        user_password = user_with_email.password

    print("Checking password : input={} real={}".format(password, user_password))
    if user_password != password:
        print("Password does not match")
        return False

    return True

def send_new_message(conversation_id, author_username, new_message_text, message_image_path=''):
    new_message =   Message(message_text=new_message_text,
                            message_date=datetime.now(),
                            author_name=author_username,
                            conversation_id=conversation_id,
                            message_image_path=message_image_path)
    db.session.add(new_message)
    db.session.commit()
    return

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
