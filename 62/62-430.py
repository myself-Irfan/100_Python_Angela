import os.path
from dotenv import load_dotenv
import logging

from flask import Flask, render_template, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL, Regexp
import csv

load_dotenv('../.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('FLASK_FORM_APP_SECRET_KEY')
Bootstrap5(app)


class CafeForm(FlaskForm):
    cafe = StringField(
        'Cafe Name',
        validators=[DataRequired()]
    )
    location = StringField(
        'Cafe Location - Google Maps(URL)',
        validators=[
            DataRequired(),
            URL(message='Please enter a valid URL')
        ]
    )
    open = StringField(
        'Opening Time e.g. 8 AM',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9]{1,2}(:[0-9]{2})?\s?[APap][Mm]$',
               message="Invalid time format. Use HH:MM AM/PM."
                   )
        ]
    )
    close = StringField(
        'Closing Time e.g. 8 PM',
        validators=[
            DataRequired(),
            Regexp(
                r'^[0-9]{1,2}(:[0-9]{2})?\s?[APap][Mm]$',
                message="Invalid time format. Use HH:MM AM/PM."
            )
        ]
    )
    coffee_rating = SelectField(
        'Coffee Rating',
        choices=[('1', '☕'), ('2', '☕☕'), ('3', '☕☕☕'), ('4', '☕☕☕☕'), ('5', '☕☕☕☕☕')],
        coerce=int,
        validators=[DataRequired()]
    )
    wifi_rating = SelectField(
        'Wifi Strength Rating',
        choices=[('1', '✘'), ('2', '💪💪'), ('3', '💪💪💪'), ('4', '💪💪💪💪'), ('5', '💪💪💪💪💪'), ('6', '💪💪💪💪💪💪')],
        coerce=int,
        validators=[DataRequired()]
    )
    power_rating = SelectField(
        'Power Socket Availability',
        choices=[('1', '✘'), ('2', '🔌'), ('3', '🔌🔌🔌'), ('4', '🔌🔌🔌🔌'), ('5', '🔌🔌🔌🔌🔌'), ('6', '🔌🔌🔌🔌🔌🔌')],
        coerce=int,
        validators=[DataRequired()]
    )

    submit = SubmitField('Submit')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add', methods=['GET', 'POST'])
def add():
    form = CafeForm()
    if form.validate_on_submit():
        with open('cafe-data.csv', mode='a', encoding='utf-8') as csv_f:
            csv_f.write(f'\n{form.cafe.data},{form.location.data},{form.open.data},{form.close.data},{form.coffee_rating.data},{form.wifi_rating.data},{form.power_rating.data}')
        return redirect(url_for('cafes'))
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('cafe-data.csv', mode='r', encoding='utf-8') as csv_f:
        csv_dt = csv.reader(csv_f, delimiter=',')
        li_rows = []
        for row in csv_dt:
            li_rows.append(row)
    return render_template('cafes.html', cafes=li_rows)


if __name__ == '__main__':
    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        ]
    )

    app.run(debug=True, port=5002)
