from flask_restful import Resource
from flask import request, jsonify
from .app import app


class HelloWorld(Resource):
    def get(self):
        print(app.url_map)
        return jsonify(["hello world"])
    

todos = {}


class TodoSimple(Resource):
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}



""" from flask import render_template, request
from app import app

@app.route("/")
def index():
    context = {
        "csrf_token": app.url_map,
    }
    return render_template("index.html", context=context)


@app.route("/profile/<username>")
def profile(username: str):
    return f"Profile: {username}" """
