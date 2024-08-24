import flask
import os

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
    return "<p>Index Page<p>"




@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = c.fetchone()
    conn.close()

    if user:
        if check_password_hash(user[2], password):
            session['username'] = username
            flash('Connexion réussie!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Mot de passe incorrect', 'danger')
    else:
        flash('Utilisateur non trouvé', 'danger')

    return redirect(url_for('index'))

@app.route("/view")
def view_messages():
    engineer = database.models.Engineer.query.get(3310)
    print(engineer)
    return flask.render_template("message_view.html.jinja2", engineer=engineer)


if __name__ == "__main__":
    app.run(debug=True)


