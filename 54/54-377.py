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


@app.route('/bye', methods=['GET'])
@app.route('/bye/<name>', methods=['GET'])
def bye(name: str = 'User') -> Response:
    if not name.isalpha():
        return make_response(jsonify(message=f'Invalid input {name}'), 400)
    return make_response(jsonify(message=f'Farewell {name}'), 200)


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