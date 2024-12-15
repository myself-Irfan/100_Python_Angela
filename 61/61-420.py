import os.path
from ensurepip import bootstrap

from dotenv import load_dotenv
from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length
import logging
from flask_bootstrap import Bootstrap5


load_dotenv('../.env')

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_FORM_APP_SECRET_KEY')
bootstrap = Bootstrap5(app)


class LoginForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[
            DataRequired(message='Email is required'),
            Email(message='Enter a valid email address')
        ]
    )
    password = PasswordField(
        label='Password',
        validators=[
            DataRequired(message='Password is required'),
            Length(min=5)
        ]
    )
    submit = SubmitField(label='Log In')


@app.route('/', methods=['GET'])
def home():
    return render_template(
        'index.html'
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        logging.info(f'Received Data: {login_form.email.data} -- {login_form.password.data}')
        if login_form.email.data == 'irfan.ahmed@tallykhata.com':
            return render_template('success.html')
        return render_template('denied.html')
    return render_template(
        'login.html',
        form=login_form
    )


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

    app.run(debug=True)
