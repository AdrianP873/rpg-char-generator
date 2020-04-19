from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField

class SignUpForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')
    email = StringField('Email')
    submit = SubmitField('Sign up')

class CreateCharacterForm(FlaskForm):
    characterName = StringField('Character Name')
    characterClass = RadioField('Label', choices=[('Knight', 'Knight'), ('Sorcerer','Sorcerer')])
    createCharacter = SubmitField('Create character')


class LoginForm(FlaskForm):
    username = StringField('Username')
    password = PasswordField('Password')