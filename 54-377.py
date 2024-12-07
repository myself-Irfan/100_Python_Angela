import logging
import os.path
from flask import Flask, jsonify, Response


app = Flask(__name__)


@app.route('/', methods=['GET'])
def greet() -> Response:
    return jsonify(message='Hello World')


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