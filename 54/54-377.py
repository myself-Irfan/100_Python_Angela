import logging
import os.path
from flask import Flask, jsonify, Response, make_response

app = Flask(__name__)


@app.route('/greet', methods=['GET'])
@app.route('/greet/<name>', methods=['GET'])
def greet(name: str = 'User') -> Response:
    if not name.isalpha():
        return make_response(jsonify(message=f'Invalid input {name}'), 400)
    return make_response(jsonify(message=f'Hello {name}'), 200)


@app.route('/age', methods=['GET'])
@app.route('/age/<name>/<int:age>', methods=['GET'])
def say_age(name: str = 'User', age: int = 18) -> Response:
    try:
        if not name.isalpha():
            raise ValueError(f'Name must contain alphabetic only input')
        if not age.is_integer():
            raise ValueError(f'Age must only contain numbers')
        if age <= 0:
            raise ValueError(f'Age must be greater than 0')
        return make_response(jsonify(message=f'Dear {name}, you are {age} years old.'), 200)
    except ValueError as val_err:
        return make_response(jsonify(message=f'Invalid input: {val_err}'), 400)
    except Exception as err:
        return make_response(jsonify(message=f'Unexpected Error: {err}'), 500)


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


if __name__ == '__main__':
    setup_logging()
    app.run(debug=True)
