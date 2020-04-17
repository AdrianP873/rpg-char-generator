
import flask
from flask import render_template, request
from forms import SignUpForm
from character_form import CreateCharacterForm

app = flask.Flask(__name__)

app.config['SECRET_KEY'] = 'thecodex'


knight = {'class':'knight', 'vigor': 12, 'endurance':11,'strength':13, 'intelligence':9}
sorcerer = {'class':'sorcerer', 'vigor': 6, 'endurance':9, 'strength':7, 'intelligence':16}

       

@app.route('/', methods=['GET', 'POST'])
def home():
    form = CreateCharacterForm()
    if form.is_submitted():
        result = request.form
        print(result)
        if result.get('characterClass') == 'Knight':
            return render_template('character.html', result=result, vocation=knight)
        elif result.get('characterClass') == 'Sorcerer':
            return render_template('character.html', result=result, vocation=sorcerer)
    return render_template('create_character.html', name='Adrian', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.is_submitted():
        result = request.form
        return render_template('user.html', result=result)
    return render_template('signup.html', form=form)






app.run(debug=True)