from datetime import datetime

from database.database import db
from database.models import User, Conversation, Message


# from database.models import Engineer


def populate_database():
    print("Populating database")

    populate_users()
    populate_groups()
    populate_messages()
    return

def populate_users():
    user1 = User(username="iliaaan", email="ilian3310@gmail.com", password="motdepasse")
    user2 = User(username="foo", email="foo@bar.com", password="foobar")
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    print("All Users :", User.query.all())
    return

def populate_groups():
    group1 = Conversation(is_private=False, conversation_name="LaConvDeClasse1")
    group1.participants.append(User.query.filter_by(username="iliaaan").first())
    group1.participants.append(User.query.filter_by(username="foo").first())
    db.session.add(group1)

    group2 = Conversation(is_private=False, conversation_name="LesWatiPotes")
    group2.participants.append(User.query.filter_by(username="iliaaan").first())
    db.session.add(group2)

    conversation1 = Conversation(is_private=True, conversation_name="")
    conversation1.participants.append(User.query.filter_by(username="foo").first())
    db.session.add(conversation1)

    db.session.commit()

    print("All Conversations :", Conversation.query.all())
    return

def populate_messages():
    message1 = Message(message_text="Bonjour tout le monde !",
                       message_date=datetime.now(),
                       author_name=User.query.filter_by(username="iliaaan").first().username,
                       conversation_id=Conversation.query.filter_by(conversation_name="LaConvDeClasse1").first().conversation_id)
    db.session.add(message1)

    message2 = Message( message_text="Hellooo @iliaaan, bienvenue !",
                        message_date=datetime.now(),
                        author_name=User.query.filter_by(username="foo").first().username,
                        conversation_id=Conversation.query.filter_by(
                        conversation_name="LaConvDeClasse1").first().conversation_id)
    db.session.add(message2)

    message3 = Message(message_text="C'est bien la conv de classe ici ?",
                       message_date=datetime.now(),
                       author_name=User.query.filter_by(username="iliaaan").first().username,
                       conversation_id=Conversation.query.filter_by(conversation_name="LaConvDeClasse1").first().conversation_id)
    db.session.add(message3)

    print(Conversation.query.filter_by(is_private=True).where(Conversation.participants.any(User.username == "foo")).first())
    mp1 = Message(  message_text="salut @iliaaan, ça va ?",
                    message_date=datetime.now(),
                    author_name=User.query.filter_by(username="foo").first().username,
                    conversation_id=Conversation.query.filter_by(is_private=True).where(Conversation.participants.any(User.username == "foo")).first().conversation_id )
    db.session.add(mp1)

    db.session.commit()

    print("All Messages :", Message.query.all())
    return