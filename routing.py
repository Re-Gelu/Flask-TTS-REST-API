from .app import api
from .views import *

api.add_resource(HelloWorld, '/')
api.add_resource(TodoSimple, '/todo/<string:todo_id>/')
