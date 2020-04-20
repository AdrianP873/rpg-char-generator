from app import app, db
from flask import render_template, request, jsonify, redirect, url_for, flash
from app.forms import RegistrationForm, CreateCharacterForm, LoginForm
import sqlite3, requests
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Character
from werkzeug.urls import url_parse

# Landing page is login
# When someone logs in, take them to an index page that displays their characters
# Make create character only accessible from the index page

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

# Landing page - login to account to use rpg character generator
@app.route('/')
def home():
    if current_user.is_anonymous:
        return redirect(url_for('login'))
    else:
        chars = Character.query.filter_by(owner=current_user).first()
        if chars is not None:
            chars = Character.query.filter_by(owner=current_user)
            return render_template('home.html', title='Home', chars=chars)
        return render_template('home.html', title='Home')


# ======================================================= 


@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user already logged in, redirect them to create character
    if current_user.is_authenticated:
        return redirect(url_for('createCharacter'))
    
    form = LoginForm()
    # Instantiate the form if submitted, query database for the username submitted
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # If username doesnt exist or password is incorrect, refresh page. 
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        #  If username and password cored, register user as logged in.
        # In future pages that user navigates to, curent_user variable is set to the user
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('home')
        return redirect(next_page)
    return render_template('login.html', form=form, title="Sign In")

@app.route('/logout')
def logout():
    # User Flask_Logins logout_user() function to remove user from session
    logout_user()
    return redirect(url_for('login'))

# =======================================================

# Sign up for an account
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('createCharacter'))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign up', form=form)

# =======================================================

# Create a character and store it in the database
@app.route('/create', methods=['GET', 'POST'])
@login_required
def createCharacter():
    # Instantiate form
    
    form = CreateCharacterForm()
    if form.is_submitted():
        char = Character(name=form.characterName.data, vocation=form.characterClass.data, owner=current_user)
        db.session.add(char)
  
        if form.characterClass.data == 'Knight':
            char.vigor = 12
            char.endurance = 11
            char.strength = 13
            char.intelligence = 9
        else:
            char.vigor =6
            char.endurance = 9
            char.strength = 7
            char.intelligence = 16

        db.session.commit()
        
        return render_template('character.html', character=form)
    return render_template('create_character.html', name='Adrian', form=form, title="Create Character")

# =======================================================

# Search for a character in the database
@app.route('/search', methods=['GET','POST'])
@login_required
def searchCharacter():
    if request.method == 'POST':
        data = request.get_json()
        character = data.get('query')
        
        chars = Character.query.filter_by(name=character)
        for char in chars:
            print(char.name, char.level, char.strength)
        
        print(current_user)

    
    
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

