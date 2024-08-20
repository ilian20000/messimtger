from database.database import db


class Engineer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    site = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<Engineer {}>'.format(self.username)
