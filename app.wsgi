import os

from whattodo import create_app

try:
    string_blueprints = os.environ.get('API_BLUEPRINTS')
    if string_blueprints:
        blueprints = string_blueprints.split(":")
    else:
        blueprints = None
except Exception:
       blueprints = None


application = create_app(blueprints=blueprints)
