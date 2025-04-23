from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging
from werkzeug.exceptions import MethodNotAllowed


db = SQLAlchemy()


def setup_logging():
    """
    this sets up logging for the project
    """
    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s -> %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        ]
    )

    logging.info('Logging setup complete')


def init_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = 'iblogpostapp'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blogs-collection.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    @app.errorhandler(405)
    def handle_method_not_allowed(e: MethodNotAllowed):
        allowed = e.valid_methods if hasattr(e, 'valid_methods') else None
        return jsonify({
            'error': f'Method {request.method} not allowed on this endpoint.',
            'allowed': allowed
        })

    from blogapp_routes import main
    from userapp_routes import userapp

    app.register_blueprint(main)
    app.register_blueprint(userapp)

    with app.app_context():
        db.create_all()

    return app
