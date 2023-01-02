
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_restful import Api
from flasgger import Swagger
from celery import Celery
import os
import config

# Flask appp
app = Flask(__name__)
app.config.from_object(os.getenv('FLASK_ENV') or 'config.DevelopementConfig')

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
#swagger = Swagger(app)
#toolbar = DebugToolbarExtension(app)

#from API import APIblueprint
#app.register_blueprint(APIblueprint)

#from .views import *
from .routing import *
