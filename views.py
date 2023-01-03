from flask import send_from_directory
from flask_restful import Resource
from flask import request, jsonify, render_template
from flask_restful import reqparse
from celery.result import AsyncResult
from werkzeug.utils import secure_filename
import werkzeug
import os
from app import app
from app import celery
from tasks import *

@app.route('/')
def index():
    context = {
        "site_map": app.url_map
    }
    return render_template('index.html', context=context)


@app.route('/uploads/audios/<name>')
def download_file(name):
    return send_from_directory(f"{app.config['UPLOAD_FOLDER']}/audios", name)


class TextToVoiceAPIViewGET(Resource):
    
    def get(self, task_id: str):
        task_result = celery.AsyncResult(task_id)
        return {
            "task_id": task_id,
            "task_result": task_result.result,
            "task_status": task_result.status,
            "task_retries": task_result.retries,
            "is_successful": task_result.successful(),
            "is_failed": task_result.failed(),
            "is_ready": task_result.ready(),
        }


class TextToVoiceAPIViewPOST(Resource):
    
    @staticmethod
    def is_allowed(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config.get("ALLOWED_EXTENSIONS")

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
            return {
                "task_id": task.id,
                "task_status": task.status,
                "task_retries": task.retries,
                "is_successful": task.successful(),
                "is_failed": task.failed(),
                "is_ready": task.ready(),
            }, 202

        return jsonify(False)
        # curl -v -X POST -H "Content-Type: multipart/form-data" -F "file=@text.txt" http://localhost:5000/api/tts
