from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess key'

class PantallaPasoUno(FlaskForm):
    fecha = DateField(validators=[DataRequired()])
    establecimiento = StringField(validators=[DataRequired()])
    localidad = StringField(validators=[DataRequired()])
    siguiente = SubmitField("Siguiente")

@app.route('/index', methods = ['GET', 'POST'])
def index():
	form = PantallaPasoUno()

	if request.method=='POST' and form.validate():
		session['fecha']=form.fecha.data
		session['establecimiento']=form.establecimiento.data
		session['localidad']=form.localidad.data
		return redirect(url_for('paso2'))
	return render_template('index.html', form=form)
	
@app.route('/paso2')
def paso2():
	return render_template('paso2.html')
# q