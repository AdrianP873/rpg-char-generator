"""
Defines the forms to be used within the applications.
"""

from flask_wtf import FlaskForm
from wtforms import (BooleanField, PasswordField, RadioField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from app.models import Character, User


class RegistrationForm(FlaskForm):
    """ The RegistrationForm class defines the attributes associated
    with the RegistrationForm """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Register")

    def validate_username(self, username):
        """ Checks that the username does not already exist. """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")

    def validate_email(self, email):
        """ Checks the email is not already in use. """
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError("Please use a different email address.")


class CreateCharacterForm(FlaskForm):
    """ Defines the attributes for the CreateCharacterForm """
    characterName = StringField("Character Name")
    characterClass = RadioField(
        "Label", choices=[("Knight", "Knight"), ("Sorcerer", "Sorcerer")]
    )
    createCharacter = SubmitField("Create character")


class LoginForm(FlaskForm):
    """ Defines the required attributes for logging in. """
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")


class SearchForm(FlaskForm):
    """ Defines the attributes used for searching characters. """
    characterName = StringField("Character Name")
    submit = SubmitField("Search")

    def validate_character(self, character_name):
        """ Checks that character does not already exist. """
        char = Character.query.filter_by(name=character_name.data).first()
        if char is None:
            raise ValidationError("That character does not exist")
