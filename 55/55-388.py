from random import randint
from flask import Flask, jsonify, Response, make_response


app = Flask(__name__)


def get_num() -> int:
    return randint(0, 9)

@app.route('/', methods=['GET'])
def guess() -> Response:
    return make_response(jsonify(message='Guess the number between 0 and 9'))

@app.route('/<int:number>', methods=['POST'])
def post_guess(number: int) -> Response:
    global num

    if number == num:
        return make_response(jsonify(message='You guessed it'), 200)
    elif number > num:
        return make_response(jsonify(message='Too High'), 200)
    elif number < num:
        return make_response(jsonify(message='Too Low'), 200)
    else:
        return make_response(jsonify(message='What?'), 400)


if __name__ == '__main__':
    num = get_num()
    app.run(debug=True)
