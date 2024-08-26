from database.database import db
from database.models import User
# from database.models import Engineer


def clear_database():
    User.query.delete()

    print("Users", db.session.query(User).all())

def populate_database():
    clear_database()
    print("Populating database")

    new_user = User(username="iliaaan", email="ilian3310@gmail.com", password="motdepasse")
    db.session.add(new_user)
    db.session.commit()
    print("Users", db.session.query(User).all())
    return
