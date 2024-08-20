from database.database import db
from database.models import Engineer


def clear_database():
    Engineer.query.delete()
    print("CLEAR ?", db.session.query(Engineer).all())

def populate_database():
    clear_database()
    new_engie = Engineer(id=3310, username="iliaaan", email="myemailgmailcom", site="bullshitco")

    db.session.add(new_engie)
    db.session.commit()
    return
