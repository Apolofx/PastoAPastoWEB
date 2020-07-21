from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import Form, FieldList, FormField, IntegerField, StringField, \
        SubmitField


class LapForm(Form):
    """Subform.

    CSRF is disabled for this subform (using `Form` as parent class) because
    it is never used by itself.
    """
    runner_name = StringField('Runner name')
    lap_time = IntegerField('Lap time')


class MainForm(FlaskForm):
    """Parent form."""
    laps = FieldList(
        FormField(LapForm),
        min_entries=1,
        max_entries=20
    )


# Create models
db = SQLAlchemy()


class Race(db.Model):
    """Stores races."""
    __tablename__ = 'races'

    id = db.Column(db.Integer, primary_key=True)


class Lap(db.Model):
    """Stores laps of a race."""
    __tablename__ = 'laps'

    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('races.id'))

    runner_name = db.Column(db.String(100))
    lap_time = db.Column(db.Integer)

    # Relationship
    race = db.relationship(
        'Race',
        backref=db.backref('laps', lazy='dynamic', collection_class=list)
    )



# Initialize app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'sosecret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db.init_app(app)
db.create_all(app=app)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MainForm()

    if form.validate_on_submit():
        # Create race
        new_race = Race()

        db.session.add(new_race)

        for lap in form.laps.data:
            new_lap = Lap(**lap)

            # Add to race
            new_race.laps.append(new_lap)

        db.session.commit()

    races = Race.query

    return render_template(
        'index.html',
        form=form,
        races=races
    )


@app.route('/<race_id>', methods=['GET'])
def show_race(race_id):
    """Show the details of a race."""
    race = Race.query.filter_by(id=race_id).first()

    return render_template(
        'show.html',
        race=race
    )


if __name__ == '__main__':
    app.run()