from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
import logging


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


def create_app():
    load_dotenv()

    app = Flask(__name__)
    app.secret_key = os.getenv('FLASK_FORM_APP_SECRET_KEY')

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books-collection.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes import main

    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app