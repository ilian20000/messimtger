from sqlalchemy.orm import backref

from database.database import db


class User(db.Model):
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(64),  unique=True, nullable=False)
    username = db.Column(db.String(64),  primary_key=True)
    email = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(64), unique=False, nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


user_conversation_table = db.Table('user_group_table',
                                    db.Column("username", db.String(64), db.ForeignKey('user.username')),
                                    db.Column("conversation_id", db.Integer, db.ForeignKey('conversation.conversation_id')))


class Conversation(db.Model):
    conversation_id = db.Column(db.Integer, primary_key=True)
    is_private = db.Column(db.Boolean(), unique=False, nullable=False)
    conversation_name = db.Column(db.String(64), unique=False, nullable=True)
    participants = db.relationship('User', backref="conversations", secondary=user_conversation_table)

    def __repr__(self):
        return '<Conversation {} {} ({} members)>'.format(self.conversation_id, self.conversation_name, len(self.participants))


class Message(db.Model):
    message_id = db.Column(db.Integer, primary_key=True)
    message_text = db.Column(db.String(64), unique=False, nullable=False)
    message_date = db.Column(db.DateTime, unique=False, nullable=False)

    author_name = db.Column(db.String(64), db.ForeignKey('user.username'), nullable=False)
    author = db.relationship('User', backref=db.backref('messages', lazy=True))

    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.conversation_id'), nullable=False)
    conversation = db.relationship('Conversation', backref=db.backref('messages', lazy=True))

    def __repr__(self):
        return '<Message {} {} at {} : {}>'.format(self.message_id, self.author, self.message_date, self.message_text)



# class Engineer(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     site = db.Column(db.String(120), unique=True, nullable=False)
#
#     def __repr__(self):
#         return '<Engineer {}>'.format(self.username)

