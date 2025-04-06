import logging
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, send_from_directory
from marshmallow import ValidationError

from auth_app import db

from model import User
from schemas import UserSchema


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

            new_user = User(
                email=user_data.get('email'),
                name=user_data.get('name'),
                password=user_data.get('password')
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

@userapp.route('/login')
def login():
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