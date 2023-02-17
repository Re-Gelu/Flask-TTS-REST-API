import os
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:

    # Flask settings

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'A SECRET KEY'

    # ORM settings

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Files settings

    STATIC_FOLDER = 'static'

    TEMPLATES_FOLDER = 'templates'

    UPLOAD_FOLDER = 'upload'

    DOWNLOAD_FOLDER = 'download'

    ALLOWED_EXTENSIONS = ['txt', 'pdf', 'rtf']

    MAX_CONTENT_LENGTH = 24 * 1000 * 1000  # 24 Mb

    # Redis settings

    REDIS_URL = 'redis://localhost:6379'

    # Celery settings

    CELERY_BROKER_URL = REDIS_URL

    RESULT_BACKEND = REDIS_URL

    CELERY_RESULT_EXPIRE_TIME = 60 * 60 * 4  # 4 hours

    TASK_SERIALIZER = "json"

    # Timezone settings

    TIMEZONE = 'Europe/Moscow'

    # Cache settings

    CACHE_TYPE = "RedisCache"

    CACHE_DEFAULT_TIMEOUT = 3600

    # TTS settings

    # Name of the pyttsx3.drivers module to load and use. Defaults to the best available driver for the platform, currently:

    # sapi5 - SAPI5 on Windows
    # nsss - NSSpeechSynthesizer on Mac OS X
    # espeak - eSpeak on every other platform

    TTS_DRIVER_NAME = None

    TTS_USE_AI_GPU = False

    TTS_AI_MODEL_ID = 7

    # Flask limiter settings

    RATELIMIT_STORAGE_URI = REDIS_URL

    RATELIMIT_DEFAULT = "50/day;5/hour"


class DevelopementConfig(BaseConfig):

    # Flask settings

    DEBUG = True

    ENV = 'development'

    # Redis settings

    REDIS_URL = 'redis://localhost:6379'

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

    RESULT_BACKEND = REDIS_URL

    # ORM settings

    SQLALCHEMY_DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI') or "sqlite:///project.db"