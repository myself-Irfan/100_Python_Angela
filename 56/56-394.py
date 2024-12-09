import os.path
from flask import Flask, render_template
import logging


app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')


if __name__ == '__main__':
    cur_f_name = os.path.splitext(os.path.basename(__file__))[0]

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s -> %(funcName)s | %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(f'{cur_f_name}.log')
        ]
    )

    app.run(debug=True)