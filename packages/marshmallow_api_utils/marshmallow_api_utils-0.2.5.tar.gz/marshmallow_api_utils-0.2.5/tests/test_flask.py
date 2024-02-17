from flask import Flask

from marshmallow_api_utils.middleware.flask_logging_middleware import FlaskLoggingMiddleware


def test_flask_logger():
    app = Flask('test')
    FlaskLoggingMiddleware(app)
