from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

# to update the database schema you have to:
# 1. Generate the migration script: flask db migrate -m "optional comment"
# 2. Run the migration script: flask db upgrade
# 3. You can revert a change or go to older version with: flask db downgrade

# For querying database via SQLalchemy see http://packages.python.org/Flask-SQLAlchemy/index.html

# The @login.user_loader decorater registers the user loader with Flask_Login
@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Inherit from the UserMixin for user login
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    characters = db.relationship('Character', backref='owner', lazy='dynamic')

    # Tell python how to print objects of the User class
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True)
    vocation = db.Column(db.String(32))
    level = db.Column(db.Integer, index=True, default=1)
    created_at = db.Column(db.DateTime, default=datetime.now)
    vigor = db.Column(db.Integer)
    endurance = db.Column(db.Integer)
    strength = db.Column(db.Integer)
    intelligence = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Character {}>'.format(self.name)



