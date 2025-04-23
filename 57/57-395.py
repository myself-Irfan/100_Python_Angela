#main

from blog_app import init_app, setup_logging


if __name__ == '__main__':
    setup_logging()
    app = init_app()
    app.run(debug=True)

    # TODO Use Flask-login
    # TODO Use JWT
    # TODO proper response format