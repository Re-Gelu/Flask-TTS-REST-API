from flask_restful import Resource
from flask import request
from app import app

class HelloWorld(Resource):
    def get(self):
        print(app.url_map)
        return ["hello world"]


todos = {}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}
