from flask import Flask


app = Flask(__name__)

def make_italic(func):
    def wrapper_func():
        str = f'<i>{func()}</i>'
        return str
    return wrapper_func


@app.route('/greet', methods=['GET'])
@make_italic
def greet():
    return 'Hello'


if __name__ == '__main__':
    app.run(debug=True)