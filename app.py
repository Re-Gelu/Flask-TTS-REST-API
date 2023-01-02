
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_caching import Cache
from flask_restful import Api
from flasgger import Swagger
from celery import Celery
import os
from . import config

# Flask app
app = Flask(__name__)
app.config.from_object(os.getenv('FLASK_ENV') or 'config.DevelopementConfig')
app.add_url_rule("/uploads/<filename>", endpoint="uploads", build_only=True)

# Celery app
celery = Celery(
    app.name,
    broker=app.config.get('REDIS_URL'),
    backend=app.config.get('REDIS_URL')
)
celery.conf.update(app.config)
celery.autodiscover_tasks()

# Flask setup
api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
cache = Cache(app)
#swagger = Swagger(app)
#toolbar = DebugToolbarExtension(app)

#from API import APIblueprint
#app.register_blueprint(APIblueprint)

#from .views import *
from .routing import *
