"""
The routes.py file defines URLs in the application which
map to python functions.
"""


from flask import flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.urls import url_parse

from app import app, db
from app.forms import (CreateCharacterForm, LoginForm, RegistrationForm,
                       SearchForm)
from app.models import Character, User


@app.route("/banana")
def hello():
    """ Test String """
    return "banana"


@app.after_request
def after_request(response):
    """ This function prevents caching during development """
    response.headers["Cache-Control"] = "no-store"
    response.headers["Expires"] = "0"
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def home():
    """ The home function renders  the homepage when landing on /.
    If not logged in, the user will be routed to the login page. """
    if current_user.is_anonymous:
        return redirect(url_for("login"))

    chars = Character.query.filter_by(owner=current_user).first()
    if chars is None:
        return render_template("home.html", title="Home")
    chars = Character.query.filter_by(owner=current_user)
    return render_template("home.html", title="Home", chars=chars)


@app.route("/login", methods=["GET", "POST"])
def login():
    """ The login function renders the login page. If user is already
    logged in they are redirected to the create character page. """
    if current_user.is_authenticated:
        return redirect(url_for("createCharacter"))

    form = LoginForm()
    # Instantiate form if submitted, query database for username
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # If username doesnt exist or password is incorrect, refresh page.
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        # If username and password cored, register user as logged in.
        # Set current_user variable to  user in future pages
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("home")
        return redirect(next_page)
    return render_template("login.html", form=form, title="Sign In")


@app.route("/logout")
def logout():
    """ The logout function removes user from their session and
    redirects user to the login page. """
    logout_user()
    return redirect(url_for("login"))


@app.route("/signup", methods=["GET", "POST"])
def signup():
    """ The signup function registers users with the application. GET requests
    to /signup will render the signup form. Submission of the form will send a
    POST to /signup and add form data to database. """
    if current_user.is_authenticated:
        return redirect(url_for("createCharacter"))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("signup.html", title="Sign up", form=form)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create_character():
    """ Renders the create character page. Submission of the character
    form adds form data to database and associates with user. """

    form = CreateCharacterForm()
    if form.is_submitted():
        char = Character(
            name=form.characterName.data,
            vocation=form.characterClass.data,
            owner=current_user,
        )
        db.session.add(char)

        if form.characterClass.data == "Knight":
            char.vigor = 12
            char.endurance = 11
            char.strength = 13
            char.intelligence = 9
        else:
            char.vigor = 6
            char.endurance = 9
            char.strength = 7
            char.intelligence = 16

        db.session.commit()

        return render_template("character.html", character=form)
    return render_template(
        "create_character.html", name="Adrian", form=form, title="Create Character"
    )


@app.route("/search", methods=["GET", "POST"])
@login_required
def search_character():
    """ Provides a search function to lookup existing characters """
    form = SearchForm()
    if form.is_submitted():
        char = Character.query.filter_by(name=form.characterName.data).first()

        if char is not None:
            return render_template("character.html", char=char)
    return render_template("search.html", title="Search Character", form=form)
