
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_restful import Api
from flasgger import Swagger
import os
import config

app = Flask(__name__)
app.config.from_object(os.getenv('FLASK_ENV') or 'config.DevelopementConfig')

api = Api(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
#swagger = Swagger(app)
#toolbar = DebugToolbarExtension(app)

#from API import APIblueprint
#app.register_blueprint(APIblueprint)

from .views import *
from .routing import *
