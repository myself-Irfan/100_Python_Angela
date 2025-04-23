import logging
from flask import Blueprint, request, jsonify, render_template, session
from marshmallow.exceptions import ValidationError

from model import db, User
from schemas import RegisterSchema, LoginSchema
from security import hash_pwd, verify_pwd


userapp = Blueprint('userapp', __name__, url_prefix='/user')

# api

@userapp.route('/api/register', methods=['POST'])
def register_user():
    register_schema = RegisterSchema()

    try:
        data = register_schema.load(request.json)

        new_user = User(
            email=data.get('email'),
            password=hash_pwd(data.get('password')),
            name=data.get('name')
        )

        db.session.add(new_user)
        db.session.commit()
    except ValidationError as valid_err:
        logging.error(f'Validation Error: {valid_err.messages}')
        return jsonify(valid_err.messages), 400
    except Exception as err:
        db.session.rollback()
        logging.error(f'An error occurred while creating user: {str(err)}')
        return jsonify({'error': 'Error occurred'}), 500
    else:
        return jsonify({'message': f'User created successfully: id-{new_user.id}'}), 201

@userapp.route('/api/login', methods=['POST'])
def login_user():
    login_schema = LoginSchema()

    try:
        data = login_schema.load(request.json)
        cur_usr_in = User(**data)

        cur_usr_db = User.query.filter_by(email=cur_usr_in.email).first()
        logging.info(f'Fetched User: {cur_usr_db.email} {cur_usr_db.password}')
    except ValidationError as valid_err:
        logging.error(f'Validation Error: {valid_err.messages}')
        return jsonify(valid_err.messages), 400
    except Exception as err:
        logging.error(f'An error occurred while creating user: {str(err)}')
        return jsonify({'error': 'Unexpected error'}), 500
    else:
        if cur_usr_db:
            logging.info('User exists! Attempting to verify password')
            if verify_pwd(cur_usr_db.password, cur_usr_in.password):
                session['user_id'] = cur_usr_db.id
                return jsonify({'message': f'User-{cur_usr_db.name} logged in successfully'}), 200
            else:
                logging.info('Incorrect password')
                return jsonify({'message': f'Incorrect password for User-{cur_usr_db.name}'})
        else:
            logging.info('User does not exist')
            return jsonify({'error': f'{cur_usr_in.email} does not exist'}), 404

@userapp.route('/api/logout', methods=['POST'])
def logout_user():
    if 'user_id' in session:
        session.clear()
        return jsonify({'message': 'User logged out successfully'}), 200
    else:
        return jsonify({'error': 'User not logged in'}), 400

