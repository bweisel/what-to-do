import os
from datetime import timedelta

DEBUG = False
TESTING = False

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Flask-JWT
JWT_EXPIRATION_DELTA = timedelta(seconds=2592000)  # Override token expiration to 30 days
JWT_AUTH_URL_RULE = '/api/auth'  # Override auth API URL
JWT_AUTH_USERNAME_KEY = 'email'  # Override auth request body (username -> email)

SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = os.environ['SECRET_KEY']

LOGGING_CONFIG = {
    'version': 1,
    'root': {
        'level': 'NOTSET',
        'handlers': ['default'],
    },
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s: %(levelname)s / %(name)s] %(message)s',
        },
    },
    'handlers': {
        'default': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'whattodo': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False,
        }
    }
}
