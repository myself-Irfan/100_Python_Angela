from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import logging


db = SQLAlchemy()


def setup_logging():
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
    app.secret_key = 'iuserapp'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///user-auth.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    from routes import userapp

    app.register_blueprint(userapp)

    with app.app_context():
        db.create_all()

    return app