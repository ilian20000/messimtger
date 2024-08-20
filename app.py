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

@app.route("/view")
def view_messages():
    engineer = database.models.Engineer.query.get(3310)
    print(engineer)
    return flask.render_template("message_view.html.jinja2", engineer=engineer)


if __name__ == "__main__":
    app.run(debug=True)


