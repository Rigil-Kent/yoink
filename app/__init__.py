from distutils.command.config import config
from flask import Flask
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import configuration, DevelopmentConfig, TestingConfig, ProductionConfig



mail =Mail()
moment = Moment()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(configuration[config_name])
    configuration[config_name].init_app(app)

    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    from .main import main as main_blueprint
    
    app.register_blueprint(main_blueprint)

    return app