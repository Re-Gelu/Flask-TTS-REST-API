from flask import Blueprint

APIblueprint = Blueprint('API', __name__)

from . import views
from . import routing