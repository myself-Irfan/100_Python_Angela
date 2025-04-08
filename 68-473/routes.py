import logging
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, send_from_directory
from marshmallow import ValidationError

from auth_app import db
from model import User
from schemas import UserSchema
from security import hash_pwd, verify_pwd


userapp = Blueprint('userapp', __name__)
user_schema = UserSchema()


@userapp.route('/')
def home():
    return render_template('index.html')

@userapp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            user_data = user_schema.load(request.form)

            hashed_pwd = hash_pwd(user_data.get('password'))
            logging.info(f'Hashed password: {hashed_pwd}')

            new_user = User(
                email=user_data.get('email'),
                name=user_data.get('name'),
                password=hashed_pwd
            )

            db.session.add(new_user)
            db.session.commit()

            return redirect(
                url_for(
                    'userapp.secrets',
                    name=new_user.name
                )
            )

        except ValidationError as val_err:
            logging.warning(f'Validation error: {val_err}')
            return render_template(
                'register.html',
                errors=val_err.messages,
                data=request.form
            )

    return render_template(
        'register.html',
        errors={},
        data=request.form
    )

@userapp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        pwd = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        logging.info(f'Fetched user: {user.email} {user.password}')

        if user:
            logging.info('User Exists! Attempting to verify password')
            if verify_pwd(user.password, pwd):
                logging.info('Logged in!!')
            else:
                logging.info('Incorrect pwd')
        else:
            logging.info('User does not exist!')

    return render_template('login.html')

@userapp.route('/secrets')
def secrets():
    name = request.args.get('name')
    return render_template('secrets.html', name=name)

@userapp.route('/logout')
def logout():
    pass

@userapp.route('/download')
def download():
    return send_from_directory(
        'static',
        path='files/cheat_sheet.pdf',
        # as_attachment=True
    )