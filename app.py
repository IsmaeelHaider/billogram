from flask import Flask

from blueprints.discount.view import discount_blueprint
from config import DevConfig
from extensions import cors

from models.models import *


def create_app(config_class=DevConfig):
    """
    Creates app with given config class
    :param config_class:
    :return: flask app object
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register Blueprints
    app.register_blueprint(discount_blueprint, url_prefix='/api/v1/discount/')

    # Boot up app extensions.
    extensions(app)

    # Register models
    with app.app_context():
        db.create_all()
    return app


def extensions(current_app):
    """
    Register 0 or more extensions (mutates the app passed in).
    :param current_app: Flask application instance
    :return: None
    """
    cors.init_app(current_app)
    db.init_app(current_app)


app = create_app()


@app.route('/', endpoint="public-indexPage")
def home():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(app, host='0.0.0.0', port='9000', debug=True)
