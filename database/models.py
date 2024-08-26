from database.database import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), unique=False, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    is_private = db.Column(db.Boolean(), unique=False, nullable=False)
    group_name = db.Column(db.String(64), unique=False, nullable=True)

    def __repr__(self):
        return '<Group {}>'.format(self.group_name)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # author = db.relationship('User', backref=db.backref('message', lazy=True))
    # message_group = db.relationship('Conversation', backref=db.backref('message', lazy=True))
    message_text = db.Column(db.String(64), unique=False, nullable=False)
    message_date = db.Column(db.DateTime, unique=False, nullable=False)

    def __repr__(self):
        return '<Message by {} : {}>'.format(self.author, self.message_text)



# class Engineer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     site = db.Column(db.String(120), unique=True, nullable=False)
#
#     def __repr__(self):
#         return '<Engineer {}>'.format(self.username)

