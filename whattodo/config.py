import os

DEBUG = False
TESTING = False

PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

SQLALCHEMY_DATABASE_URI = 'sqlite:////Users/bweisel/Code/what-to-do/what-to-do.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True

SECRET_KEY = 'this-is-the-local-key'

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
