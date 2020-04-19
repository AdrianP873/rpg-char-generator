from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired

class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Sign up')

class CreateCharacterForm(FlaskForm):
    characterName = StringField('Character Name')
    characterClass = RadioField('Label', choices=[('Knight', 'Knight'), ('Sorcerer','Sorcerer')])
    createCharacter = SubmitField('Create character')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Login")