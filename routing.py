from .app import api
from .views import *

api.add_resource(HelloWorld, '/api')
api.add_resource(TodoSimple, '/api/todo/<string:todo_id>/')
