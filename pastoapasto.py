from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hard to guess key'

class PantallaPasoUno(FlaskForm):
    fecha = DateField(validators=[DataRequired()])
    establecimiento = StringField(validators=[DataRequired()])
    localidad = StringField(validators=[DataRequired()])


@app.route('/index', methods = ['GET', 'POST'])
def index():
    form = PantallaPasoUno()

    return render_template('index.html', form=form)
