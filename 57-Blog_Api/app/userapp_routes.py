import logging
from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from marshmallow.exceptions import ValidationError

from .model import db, User
from .schemas import RegisterSchema, LoginSchema
from .security import hash_pwd, verify_pwd

userapp = Blueprint('userapp', __name__, url_prefix='/user')


def gen_token(user_id: str):
    return create_access_token(identity=user_id), create_refresh_token(identity=user_id)

# api

@userapp.route('/api/register', methods=['POST'])
def register_user():
    register_schema = RegisterSchema()

    try:
        data = register_schema.load(request.json)

        email = data.get('email')

        if User.query.filter_by(email=email).first():
            return jsonify({
                'status': 'warning',
                'message': f'Email-{email} already in use'
            }), 400

        new_user = User(
            email=email,
            password=hash_pwd(data.get('password')),
            name=data.get('name')
        )

        db.session.add(new_user)
        db.session.commit()
    except ValidationError as valid_err:
        logging.error(f'Validation Error: {valid_err.messages}')
        return jsonify({
            'status': 'warning',
            'message': valid_err.messages
        }), 400
    except Exception as err:
        db.session.rollback()
        logging.error(f'An error occurred while creating user: {str(err)}')
        return jsonify({
            'status': 'error',
            'message': 'Unexpected error occurred'
        }), 500
    else:
        return jsonify({
            'status': 'success',
            'message': f'User created successfully: id-{new_user.id}'
        }), 201

@userapp.route('/api/login', methods=['POST'])
def login_user():
    login_schema = LoginSchema()

    try:
        data = login_schema.load(request.json)
        email = data.get('email')
        password = data.get('password')

        cur_usr_db = User.query.filter_by(email=email).first()
    except ValidationError as valid_err:
        logging.error(f'Validation Error: {valid_err.messages}')
        return jsonify(valid_err.messages), 400
    except Exception as err:
        logging.error(f'An error occurred while logging user in: {str(err)}')
        return jsonify({
            'status': 'error',
            'message': 'Unexpected error'
        }), 500
    else:
        if cur_usr_db:
            logging.info('User exists! Attempting to verify password')
            if verify_pwd(cur_usr_db.password, password):
                access_token, refresh_token = gen_token(str(cur_usr_db.id))
                return jsonify({
                    'status': 'success',
                    'message': f'User-{cur_usr_db.name} logged in successfully',
                    'data': {
                        'access_token': access_token,
                        'refresh_token': refresh_token
                    }
                }), 200
            else:
                logging.info('Incorrect password')
                return jsonify({
                    'status': 'warning',
                    'message': f'Incorrect password for User-{cur_usr_db.name}'
                }), 401
        else:
            logging.info('User does not exist')
            return jsonify({
                'status': 'warning',
                'message': f'{email} does not exist'
            }), 404

@userapp.route('/api/refresh-token', methods=['POST'])
@jwt_required(refresh=True)
def refresh_token():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    return jsonify(access_token=new_access_token)

# template

@userapp.route('/login')
def login():
    return render_template('login.html')

@userapp.route('/register')
def register():
    return render_template('register.html')
