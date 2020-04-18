import flask
from flask import render_template, request, jsonify
from forms import SignUpForm
from character_form import CreateCharacterForm
import sqlite3
import requests

app = flask.Flask(__name__)
app.config['SECRET_KEY'] = 'mySecretKey'

# Function to convert database cursor objects into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Create character page
@app.route('/', methods=['GET', 'POST'])
def home():
    
    # Instantiate form
    form = CreateCharacterForm()

    # Get form data and pass it to template for rendering
    if form.is_submitted():
        result = request.form
        if result.get('characterClass') == 'Knight':
            vocation = {'class':'knight', 'level':1, 'vigor': 12, 'endurance':11,'strength':13, 'intelligence':9}
        else:
            vocation = {'class':'sorcerer', 'level':1, 'vigor': 6, 'endurance':9, 'strength':7, 'intelligence':16}
        
        # Add character data into database ||| to be completed after GET character
        resultList = []
        resultList.append(result.get('characterName'))
        resultList.append(result.get('characterClass'))
        resultList.append(vocation.get('level'))
        resultList.append(vocation.get('vigor'))
        resultList.append(vocation.get('endurance'))
        resultList.append(vocation.get('strength'))
        resultList.append(vocation.get('intelligence'))
        print(resultList)

        conn = sqlite3.connect('rpg.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute('INSERT INTO Characters VALUES (?,?,?,?,?,?,?)', resultList)
        conn.commit()
        conn.close()
        

        return render_template('character.html', result=result, vocation=vocation)
    return render_template('create_character.html', name='Adrian', form=form)



# Get characters from database
@app.route('/search', methods=['POST'])
def searchCharacter():
    data = request.get_json()
    character = data.get('query')
    
    resList = [character]

    conn = sqlite3.connect('rpg.db')
    conn.row_factory = dict_factory
    cur =  conn.cursor()
    
    char = cur.execute('SELECT * FROM Characters WHERE Name = ? ;', resList).fetchone()

    if char != None:
        return render_template('character.html', char=char)
    else:
        return "That character does not exist"

# =======================================================

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result=result)
    return render_template('signup.html', form=form)

app.run(debug=True)