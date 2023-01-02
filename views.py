from flask_restful import Resource
from flask import request, jsonify, render_template
from .app import app
from .tasks import *

@app.route('/')
def index():
    context = {
        "site_map": app.url_map
    }
    return render_template('index.html', context=context)

class HelloWorld(Resource):
    def get(self):
        print(app.url_map)
        return jsonify(["hello world"])
    

class TaskRunnerView(Resource):

    def post(self):
        content = request.json
        task_type = content["type"]
        task = create_task.delay(int(task_type))
        return jsonify({"task_id": task.id})

todos = {}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}


""" class TextToVoiceAPI(Resource):
    def get(self, todo_id): """
