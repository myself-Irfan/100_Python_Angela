# main

from app import create_app, setup_logging


if __name__ == '__main__':
    setup_logging()
    app = create_app()
    app.run(debug=True)