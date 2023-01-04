from flask import send_from_directory
from flask_restful import Resource
from flask import request, jsonify, render_template, url_for
from flask_restful import reqparse
from werkzeug.utils import secure_filename
import werkzeug
import pyttsx3
import os
from app import app
from app import api
from app import celery
from tasks import *
import datetime

@app.route('/')
def index():
    context = {
        "site_map": app.url_map
    }
    return render_template('index.html', context=context)


@app.route('/download/audio/<filename>')
def download_file(filename):
    return send_from_directory(f"{app.config['DOWNLOAD_FOLDER']}/audio", filename)


class TaskResultAPIView(Resource):
    
    def get(self, task_id: str):
        task_result = celery.AsyncResult(task_id)
        task_result_url = None
        
        if '/' + task_result.result == url_for('download_file', filename=os.path.basename(task_result.result)):
            task_result_url = f"{request.scheme}://{request.headers.get('HOST')}/{task_result.result}"
            
        return {
            "task_id": task_id,
            "task_result": str(task_result.result),
            "task_result_url": task_result_url,
            "task_status": task_result.status,
            "date_done": str(task_result.date_done),
            "expires": str(task_result.date_done + datetime.timedelta(seconds=app.config.get('CELERY_RESULT_EXPIRE_TIME'))) if task_result.date_done else str(datetime.datetime.now()),
            "task_retries": task_result.retries,
            "is_successful": task_result.successful(),
            "is_failed": task_result.failed(),
            "is_ready": task_result.ready(),
        }, 200
        
    def delete(self, task_id):
        celery.control.revoke(task_id)
        return {
            "task_id": task_id,
            "is_deleted": True,
        }, 200


class TextToVoiceAPIView(Resource):
    
    @staticmethod
    def is_allowed(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config.get("ALLOWED_EXTENSIONS")
    
    def get(self):
        return {
            "upload_args_names": ["file", "text", "voice_rate", "voice_volume", "voice_id"],
            "voices_ids": [
                {
                    key: {
                        "name": voice.name, 
                        "languages": voice.languages, 
                        "gender": voice.gender, 
                        "age": voice.age
                    }
                } for key, voice in enumerate(pyttsx3.init().getProperty('voices'))
            ],
            "allowed_extensions": app.config.get('ALLOWED_EXTENSIONS'),
            "task_statuses": ["PENDING", "STARTED", "RETRY", "FAILURE", "SUCCESS"],
            "max_content_length": app.config.get('MAX_CONTENT_LENGTH'),
            "download_url": f"{app.config.get('DOWNLOAD_FOLDER')}/audio/"
        }, 200
        

    def post(self):
        # Get the file, text and other tts args string from the post request
        parser = reqparse.RequestParser()
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parser.parse_args()
        file = args.get('file', None)
        text = request.form.get('text', default=None)
        voice_rate = int(request.form.get('voice_rate')) if request.form.get('voice_rate') else request.form.get('voice_rate', default=None)
        voice_id = int(request.form.get('voice_id')) if request.form.get('voice_id') else request.form.get('voice_id', default=None)
        voice_volume = float(request.form.get('voice_volume')) if request.form.get('voice_volume') else request.form.get('voice_volume', default=None)
        
        file_save_path = None
        
        if text or file:
            
            if file and self.is_allowed(file.filename):
                
                # Save the file
                filename = secure_filename(file.filename)
                file_save_path = os.path.join(f"{app.config['UPLOAD_FOLDER']}/text", filename)
                file.save(file_save_path)
                
                # Create task for file
                task = text_to_voice_api_task.delay(
                    file_save_path=file_save_path,
                    voice_rate=voice_rate,
                    voice_id=voice_id,
                    voice_volume=voice_volume
                )

                return {
                    "task_id": task.id,
                    "task_url": request.base_url + '/' + task.id,
                    "task_status": task.status,
                    "task_retries": task.retries,
                    "is_successful": task.successful(),
                    "is_failed": task.failed(),
                    "is_ready": task.ready(),
                }, 202
                
            elif text:
                
                # Create task for text
                task = text_to_voice_api_task.delay(
                    text=text,
                    voice_rate=voice_rate,
                    voice_id=voice_id,
                    voice_volume=voice_volume
                )

                return {
                    "task_id": task.id,
                    "task_url": request.base_url + '/' + task.id,
                    "task_status": task.status,
                    "task_retries": task.retries,
                    "is_successful": task.successful(),
                    "is_failed": task.failed(),
                    "is_ready": task.ready(),
                }, 202
                
            else:
                
                # If not file
                return {
                    "error": "The file was not provided or the file extension is not supported!",
                    "allowed_extensions": app.config.get('ALLOWED_EXTENSIONS'),
                    "is_successful": False,
                    "is_failed": True,
                }, 400
        else:
            
            # If not the file and text
            return {
                "error": "The text or file was not provided!",
                "is_successful": False,
                "is_failed": True,
            }, 400
        # curl -v -X POST -H "Content-Type: multipart/form-data" -F "file=@text.txt" http://localhost:5000/api/tts
