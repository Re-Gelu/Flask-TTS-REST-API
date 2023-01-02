import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'
    
    TIMEZONE = 'Europe/Moscow'
    
    """ MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'mailL@mail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'password'
    MAIL_DEFAULT_SENDER = MAIL_USERNAME """


class DevelopementConfig(BaseConfig):
    DEBUG = True
    ENV = 'development'
    
    REDIS_URL = 'redis://localhost:6379'

    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or "sqlite:///project.db"


class TestingConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or "sqlite:///project.db"


class ProductionConfig(BaseConfig):
    DEBUG = False
    ENV = 'production'
    
    REDIS_URL = 'redis://redis:6379/0'
    
    CELERY_BROKER_URL = REDIS_URL
    CELERY_RESULT_BACKEND = REDIS_URL
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or "sqlite:///project.db"