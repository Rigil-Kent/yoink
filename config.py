import os
from yoink.config import config



basedir = os.path.abspath(os.path.dirname(__file__))



class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'snapekilleddumpledork')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', 465)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', False)
    MAIL_USE_SSL = os.environ.get('MAIL_USE_SSL', True)
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_PREFIX = os.environ.get('MAIL_PREFIX', '[YO!NK]')
    MAIL_SENDER = os.environ.get('MAIL_SENDER', 'YO!NK Admin <yoinkmediaapp@gmail.com>')


    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or f'sqlite:///{os.path.join(config.app_root, "data-dev.sqlite")}'


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or f'sqlite:///{os.path.join(config.app_root, "data-test.sqlite")}'

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or f'sqlite:///{os.path.join(config.app_root, "data.sqlite")}'


configuration = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}