from flask_restful import Resource
from flask import request, jsonify, render_template, url_for
from flask_restful import reqparse
import werkzeug
from werkzeug.utils import secure_filename
import os
from .app import app
from .tasks import *

@app.route('/')
def index():
    context = {
        "site_map": app.url_map
    }
    return render_template('index.html', context=context)
    

class TaskRunnerView(Resource):

    def post(self):
        content = request.json
        task_type = content["type"]
        task = create_task.delay(int(task_type))
        return jsonify({"task_id": task.id})


class TextToVoiceAPIView(Resource):
    
    @staticmethod
    def is_allowed(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config.get("ALLOWED_EXTENSIONS")
           
    def get(self):
        return jsonify(True)

    def post(self):
        # Get the file from the post request
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        file = args.get('file')
        
        # Save the file
        if file and self.is_allowed(file.filename):
            filename = secure_filename(file.filename)
            file_save_path = os.path.join(f"{app.config['UPLOAD_FOLDER']}/texts", filename)
            file.save(file_save_path)
            
            # Create task
            task = text_to_voice_api_task.delay(
                file_save_path=file_save_path
            )
            #return jsonify(url_for('uploads', filename=filename))
            return {"task_id": task.id}, 202

        return jsonify(False)
        # curl -v -X POST -H "Content-Type: multipart/form-data" -F "file=@text.txt" http://localhost:5000/api/tts
