
import flask
from flask import render_template, request
from forms import SignUpForm
from character_form import CreateCharacterForm
import sqlite3
import requests

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = 'thecodex'


knight = {'class':'knight', 'vigor': 12, 'endurance':11,'strength':13, 'intelligence':9}
sorcerer = {'class':'sorcerer', 'vigor': 6, 'endurance':9, 'strength':7, 'intelligence':16}

       
# Create character page
@app.route('/', methods=['GET', 'POST'])
def home():
    
    # Instantiate form
    form = CreateCharacterForm()

    # Get form data and pass it to template for rendering
    if form.is_submitted():
        result = request.form
        if result.get('characterClass') == 'Knight':
            vocation = knight
        else:
            vocation = sorcerer
        # Add character data into database ||| to be completed after GET character
        #conn = sqlite3.connect('rpg.db')
        #cur = conn.cursor()
        return render_template('character.html', result=result, vocation=vocation)
    return render_template('create_character.html', name='Adrian', form=form)

# Get characters from database
@app.route('/search', methods=['POST'])
def searchCharacter():
    result = request.get_json()
    name = result.get('query')

    conn = sqlite3.connect('rpg.db')
    cur =  conn.cursor()
    

    
    

    return "<h2>Hi</h2>"



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result=result)
    return render_template('signup.html', form=form)






app.run(debug=True)