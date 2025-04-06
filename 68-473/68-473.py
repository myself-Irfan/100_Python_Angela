from auth_app import setup_logging, init_app


if __name__ == '__main__':
    setup_logging()
    app = init_app()
    app.run(debug=True)