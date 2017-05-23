import logging.config
from flask import Flask
from flask_jwt import JWT
from datetime import timedelta

from whattodo import blueprints
from whattodo.extensions import db, marshmallow
from whattodo.common import auth_utils

DEFAULT_BLUEPRINTS = (
    blueprints.api_bp,
)


__all__ = ['create_app']


def create_app(blueprints=None, testing=False):
    """Create flask app and return it"""
    if blueprints is None:
        blueprints = DEFAULT_BLUEPRINTS

    app = Flask(
        'whattodo',
        instance_path='/tmp',
        instance_relative_config=True
    )

    configure_app(app, testing)
    configure_db(app)
    configure_auth(app)
    configure_blueprints(app, blueprints)
    configure_marshmallow(app)
    configure_logging(app)

    return app


def configure_app(app, testing):
    """Initialize configuration"""
    app.config.from_object('whattodo.config')

    if testing is True:
        app.config.from_object('whattodo.test_config')
    else:
        app.config.from_pyfile('config.cfg', silent=True)


def configure_db(app):
    """Initialize database"""
    db.init_app(app)


def configure_auth(app):
    """Initialize flask-jwt"""
    jwt = JWT(app, auth_utils.authenticate, auth_utils.identity)
    jwt.init_app(app)


def configure_blueprints(app, blueprints):
    """Configure blueprints in views"""
    for blueprint in blueprints:
        if isinstance(blueprint, str):
            blueprint = getattr(blueprints, blueprint)
        app.register_blueprint(blueprint)


def configure_marshmallow(app):
    """Initialize marshmallow"""
    marshmallow.init_app(app)


def configure_logging(app):
    """Configure logging"""
    logging.config.dictConfig(app.config['LOGGING_CONFIG'])
