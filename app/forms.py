from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CreateCharacterForm(FlaskForm):
    characterName = StringField('Character Name')
    characterClass = RadioField('Label', choices=[('Knight', 'Knight'), ('Sorcerer','Sorcerer')])
    createCharacter = SubmitField('Create character')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField("Login")

class SearchForm(FlaskForm):
    characterName = StringField('Character Name')
    submit = SubmitField('Search')

    def validate_character(self, characterName):
        char = Character.query.filter_by(name=characterName.data).first()
        if char is None:
            raise ValidationError('That character does not exist')


