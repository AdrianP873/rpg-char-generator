from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    # Tell python how to print objects of the User class
    def __repr__(self):
        return '<User {}>'.format(self.username)



# to update the database schema you have to:
# 1. Generate the migration script: flask db migrate -m "optional comment"
# 2. Run the migration script: flask db upgrade
# 3. You can revert a change or go to older version with: flask db downgrade
