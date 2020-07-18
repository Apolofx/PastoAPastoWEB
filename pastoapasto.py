from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, SelectField, IntegerField, FieldList, TextField, FormField
from wtforms.validators import DataRequired, NumberRange

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess key'

class PantallaPasoUno(FlaskForm):
    fecha = DateField(validators=[DataRequired()])
    establecimiento = StringField(validators=[DataRequired()])
    localidad = StringField(validators=[DataRequired()])
    siguiente = SubmitField("Siguiente")

class PantallaPasoDos(FlaskForm):
    area_cuadrante = SelectField(choices=[('1', '1 m\u00B2'), ('0.25', '0.25 m\u00B2')], validators=[DataRequired()])
    num_vacas = IntegerField(validators=[DataRequired(), NumberRange(min=1)])
    porcen_matseca = IntegerField(validators=[DataRequired(), NumberRange(min=1, max=100)])
    superf_parcela = IntegerField(validators=[DataRequired(), NumberRange(min=1)])
    recurso = StringField(validators=[DataRequired()])
    lote = StringField(validators=[DataRequired()])
    siguiente = SubmitField("Siguiente")

@app.route('/index', methods = ['GET', 'POST'])
def index():
	form = PantallaPasoUno()
	if request.method == 'POST' and form.validate():
		session['fecha'] = form.fecha.data
		session['establecimiento'] = form.establecimiento.data
		session['localidad'] = form.localidad.data
		return redirect(url_for('paso2'))
	return render_template('index.html', form=form)
	
@app.route('/paso2', methods=['GET', 'POST'])
def paso2():
	form = PantallaPasoDos()
	if request.method == 'POST' and form.validate():
		session['area-cuadrante'] = form.area_cuadrante.data
		session['numero-de-vacas'] = form.num_vacas.data
		session['porcentaje-materia-seca'] = form.porcen_matseca.data
		session['superficie-parcela'] = form.superf_parcela.data
		session['recurso'] = form.recurso.data
		session['lote'] = form.lote.data
		return redirect(url_for('paso3'))
	print(form.errors)
	return render_template('paso2.html', form=form)


class SubDirForm(FlaskForm):
    subDirName = TextField(validators=[DataRequired()])
    
class SubDirsForm(FlaskForm):
    subDirList = FieldList(FormField(SubDirForm), min_entries=0)
    siguiente = SubmitField()


@app.route('/paso3', methods=['GET', 'POST'])
def paso3():
	# user_subdirs = {}
	# subdirs = user_subdirs
	form = SubDirsForm()
	if request.method == 'POST' and form.validate():
		for entrada in form.subDirList.entries:
			return print(entrada.data)
	print(form.errors)
	return render_template('paso3.html', form=form)


# @app.route('/paso3')
# def paso3():
# 	form = PantallaPasoDos()
# 	print(session.get('establecimiento'))
# 	print(session.get('area-cuadrante'))
# 	return render_template('paso3.html', form=form)


