import os

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    
    # Flask settings
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'
    
    # ORM settings
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Files settings
    
    STATIC_FOLDER = 'static'
    
    TEMPLATES_FOLDER = 'templates'
    
    UPLOAD_FOLDER = 'uploads'

    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'rtf'}

    MAX_CONTENT_LENGTH = 24 * 1000 * 1000  # 24 Mb
    
    # Timezone settings
    
    TIMEZONE = 'Europe/Moscow'
    
    # Cache settings
    
    CACHE_TYPE = "RedisCache"
    
    CACHE_DEFAULT_TIMEOUT = 500

class DevelopementConfig(BaseConfig):
    
    # Flask settings
    
    DEBUG = True
    
    ENV = 'development'
    
    # Redis settings
    
    REDIS_URL = 'redis://localhost:6379'
    
    # Celery settings

    CELERY_BROKER_URL = REDIS_URL
    
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # ORM settings
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEVELOPMENT_DATABASE_URI') or "sqlite:///project.db"


class TestingConfig(BaseConfig):
    
    # Flask settings
    
    DEBUG = True
    
    TESTING = True
    
    # ORM settings
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('TESTING_DATABASE_URI') or "sqlite:///project.db"


class ProductionConfig(BaseConfig):
    
    # Flask settings
    
    DEBUG = False
    
    ENV = 'production'
    
    # Redis settings (prepared for docker)
    
    REDIS_URL = 'redis://redis:6379/0'
    
    # Celery settings
    
    CELERY_BROKER_URL = REDIS_URL
    
    CELERY_RESULT_BACKEND = REDIS_URL
    
    # ORM settings
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or "sqlite:///project.db"