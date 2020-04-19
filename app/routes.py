from app import app
from flask import render_template, request, jsonify, redirect, url_for, flash
from app.forms import SignUpForm, CreateCharacterForm, LoginForm
import sqlite3, requests

# =======================================================
# === Config Functions === #

# Function to convert database cursor objects into a dictionary
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# Prevent caching during development
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-store"
    response.headers["Expires"] = '0'
    response.headers["Pragma"] = "no-cache"
    return response

# ======================================================= 

# Landing page - login to account to use rpg character generator
@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requests for user {}, remember_me=[]'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('createCharacter'))
    return render_template('login.html', form=form, title="Sign In")

# =======================================================

# Create a character and store it in the database
@app.route('/create', methods=['GET', 'POST'])
def createCharacter():
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

        conn = sqlite3.connect('rpg.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        cur.execute('INSERT INTO Characters VALUES (?,?,?,?,?,?,?)', resultList)
        conn.commit()
        conn.close()

        return render_template('character.html', result=result, vocation=vocation)
    return render_template('create_character.html', name='Adrian', form=form, title="Create Character")

# =======================================================

# Search for a character in the database
@app.route('/search', methods=['GET','POST'])
def searchCharacter():
    if request.method == 'POST':
        data = request.get_json()
        character = data.get('query')
    
        queryList = [character]

        conn = sqlite3.connect('rpg.db')
        conn.row_factory = dict_factory
        cur =  conn.cursor()
    
        char = cur.execute('SELECT * FROM Characters WHERE Name = ? ;', queryList).fetchone()

        if char != None:
            return render_template('character.html', char=char, title=char.get('Name'))
        else:
            return "That character does not exist"
    return render_template('search.html', title="Search Character")

# =======================================================

# Sign up for an account
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.is_submitted():
        result = request.form
        email = result.get('email')
        return render_template('login.html', res=result)
    return render_template('signup.html', form=form)
