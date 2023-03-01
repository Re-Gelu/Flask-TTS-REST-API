from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_caching import Cache
from flask_restful import Api
from flask_cors import CORS
from flasgger import Swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from celery import Celery
import os
import config

flask_env_config = os.getenv('FLASK_ENV') or 'config.DevelopementConfig'

# Flask app
app = Flask(__name__)
app.config.from_object(flask_env_config)

# Celery app
celery = Celery(
    app.import_name,
    broker=app.config.get('REDIS_URL'),
    backend=app.config.get('REDIS_URL'),
    result_expires=app.config.get('CELERY_RESULT_EXPIRE_TIME')
)
celery.config_from_object(flask_env_config)
celery.autodiscover_tasks()

# Flask setup
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)
swagger = Swagger(app, template_file='openapi.json')
cors = CORS(app)
limiter = Limiter(
    get_remote_address,
    app=app
)
#toolbar = DebugToolbarExtension(app)

from routing import *
