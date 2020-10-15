"""
Defines the database models.
"""

from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from app import db, login


@login.user_loader
def load_user(id):
    """ Registers user with Flask_Login """
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    """ User class. Inherits UserMixin for user login. """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    characters = db.relationship("Character", backref="owner", lazy="dynamic")

    # Tell python how to print objects of the User class
    def __repr__(self):
        """ Defines how User class objects should be printed """
        return "<User {}>".format(self.username)

    def set_password(self, password):
        """ Generates a password hash. """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """ Checks that passwords match. """
        return check_password_hash(self.password_hash, password)


class Character(db.Model):
    """ Character model containing information about the character. """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    vocation = db.Column(db.String(32))
    level = db.Column(db.Integer, index=True, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now)
    vigor = db.Column(db.Integer)
    endurance = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self):
        """ Defines how Character class objects should be printed """
        return "<Character {}>".format(self.name)
