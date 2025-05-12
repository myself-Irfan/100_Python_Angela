from app.__init__ import init_app, setup_logging


# Initialize logging and app at module level for Gunicorn
setup_logging()
app = init_app()

if __name__ == '__main__':
    app.run(debug=True)