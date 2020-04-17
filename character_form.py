from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField

class CreateCharacterForm(FlaskForm):
    characterName = StringField('Character Name')
    characterClass = RadioField('Label', choices=[('Knight', 'Knight'), ('Sorcerer','Sorcerer')])
    createCharacter = SubmitField('Create character')