from flask import Flask

# local import
from instance.config import app_config

from app.api.v1.views import meetup_view_blueprint
from app.api.v1.views import question_view_blueprint

def create_api_server(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    
    app.register_blueprint(meetup_view_blueprint, url_prefix='/api/v1')
    app.register_blueprint(question_view_blueprint, url_prefix='/api/v1')

    return app
