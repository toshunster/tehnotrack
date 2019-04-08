from app import db

class Person(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    username = db.Column('nickname', db.String(90), unique=True, nullable=False)
    first_name = db.Column('second_name', db.String(90), unique=False, nullable=True)

    def __init__(self, username, first_name=''):
        self.username = username
        self.first_name = first_name


