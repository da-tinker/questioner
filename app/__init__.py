from flask import Flask

# local import
from instance.config import app_config


def create_api_server(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    return app
