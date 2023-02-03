from flask import send_from_directory
from flask_restful import Resource
from flask import request, jsonify, render_template, url_for
from flask_restful import reqparse
from werkzeug.utils import secure_filename
import werkzeug
import pyttsx3
import os
from app import app
from app import celery
from app import cache
from tasks import *
import datetime

@app.route('/')
@cache.cached()
def index(): 
    return render_template('index.html')


@app.route('/download/audio/<path:filename>')
def download_file(filename):
    return send_from_directory(f"{app.config['DOWNLOAD_FOLDER']}/audio", filename)


class TaskResultAPIView(Resource):

    @cache.cached()
    def get(self, task_id: str):
        """Get TTS task result by UUID
        ---
        parameters:
            - name: task_id
              in: path
              type: string
              format: uuid
              required: true
              description: Task UUID
        responses:
            200:
                description: TTS task result
                schema:
                    type: object
                    properties:
                        task_id:
                            type: string
                            format: uuid
                            description: UUID of the task
                            default: all
                        task_result:
                            type: string
                            default: all
                        task_result_url:
                            type: string
                            format: uri
                            description: URL to download the task result
                        date_done:
                            type: string
                            format: date-time
                        expires:
                            type: integer
                        task_status:
                            type: string
                            enum: ["PENDING", "STARTED", "RETRY", "FAILURE", "SUCCESS"]
                            description: Task status from the list of possible options
                        task_retries:
                            type: integer
                            description: Amount of retries (if task failed)
                            default: 0
                        is_successful:
                            type: boolean
                            default: true
                        is_failed:
                            type: boolean
                            default: false
                        is_ready:
                            type: boolean
                            default: true
                
        """
        task = celery.AsyncResult(task_id)
        task_result_url = None
        task_result = task.result if task.result else ''    
        
        if f"/{task_result}" == url_for('download_file', filename=os.path.basename(task_result)):
            task_result_url = f"{request.scheme}://{request.headers.get('HOST')}/{task.result}"
            
        return {
            "task_id": task_id,
            "task_result": str(task.result) if task.result else None,
            "task_result_url": task_result_url,
            "task_status": task.status,
            "date_done": str(task.date_done) if task.date_done else None,
            "expires": str(task.date_done + datetime.timedelta(seconds=app.config.get('CELERY_RESULT_EXPIRE_TIME'))) if task.date_done else str(datetime.datetime.now()),
            "task_retries": task.retries,
            "is_successful": task.successful(),
            "is_failed": task.failed(),
            "is_ready": task.ready(),
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
    
    @cache.cached()
    def get(self):
        """Main API info
        ---                 
        responses:
            200:
                description: Main API info
                schema:
                    type: object
                    properties:
                        upload_args_names:
                            type: array
                            description: List of possible arguments in POST request
                            items:
                                type: string
                        voices:
                            type: array
                            description: List of voices on the server
                            items:
                                type: object
                                properties:
                                    name:
                                        type: string
                                    languages:
                                        type: array
                                        items:
                                            type: string
                                    gender:
                                        type: string
                                    age:
                                        type: integer
                        allowed_extensions:
                            description: List of extensions that can be used
                            type: array
                            items: 
                                type: string
                                enum: ["txt", "pdf"]
                        task_statuses:
                            description: List of possible tasks statuses
                            type: array
                            items: 
                                type: string
                        max_content_length:
                            description: Maximum length of the request
                            type: integer
                        download_url:
                            description: URL to use with task id
                            type: string
                            format: url

        """
        return {
            "upload_args_names": ["file", "text", "voice_rate", "voice_volume", "voice_id"],
            "voices": [
                {
                    "name": voice.name, 
                    "languages": voice.languages, 
                    "gender": voice.gender, 
                    "age": voice.age
                } for voice in pyttsx3.init().getProperty('voices')
            ],
            "allowed_extensions": app.config.get('ALLOWED_EXTENSIONS'),
            "task_statuses": ["PENDING", "STARTED", "RETRY", "FAILURE", "SUCCESS"],
            "max_content_length": app.config.get('MAX_CONTENT_LENGTH'),
            "download_url": f"{app.config.get('DOWNLOAD_FOLDER')}/audio/"
        }, 200
        

    def post(self):
        """Create TTS task
        ---
        consumes:
            - multipart/form-data
        parameters:
            - name: text
              in: formData
              type: string
              default: all
              description: The uploaded text data
            - name: file
              in: formData
              description: The uploaded file data
              type: file
            - name: voice_rate
              in: formData
              type: integer
              default: 200
              minimum: 0
              maximum: 1000
              description: TTS voice rate
            - name: voice_id
              in: formData
              type: integer
              default: 0
              minimum: 0
              maximum: 100
              description: TTS voice id from the list in GET response
            - name: voice_volume
              in: formData
              type: number
              format: float
              default: 1.0
              minimum: 0.0
              maximum: 1.0
              description: TTS voice volume
            - name: use_AI
              in: formData
              type: boolean
              default: false
              description: Parameter to use the AI voice generation (not stable)
        responses:
            202:
                description: TTS task created successfully
                schema:
                    type: object
                    properties:
                        task_id:
                            type: string
                            format: uuid
                            description: UUID of the task
                            default: all
                        task_url:
                            type: string
                            format: uri
                            description: URL to check the task result
                        task_status:
                            type: string
                            enum: ["PENDING", "STARTED", "RETRY", "FAILURE", "SUCCESS"]
                            description: Task status from the list of possible options
                        task_retries:
                            type: integer
                            description: Amount of retries (if task failed)
                            default: 0
                        is_successful:
                            type: boolean
                            default: true
                        is_failed:
                            type: boolean
                            default: false
                        is_ready:
                            type: boolean
                            default: false
            400: 
                description: TTS task creation failed
                schema:
                    type: object
                    properties:
                        error:
                            type: string
                        allowed_extensions:
                            type: array
                            items: 
                                type: string
                        is_successful:
                            type: boolean
                            default: false
                        is_failed:
                            type: boolean
                            default: true
                            

        """
        # Parse the file, text and other tts args from the post request
        parser = reqparse.RequestParser()
        
        parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        parser.add_argument('text', type=str, location='form')
        parser.add_argument('voice_rate', type=int, location='form')
        parser.add_argument('voice_id', type=int, location='form')
        parser.add_argument('voice_volume', type=float, location='form')
        parser.add_argument('use_AI', type=bool, location='form')
        
        args = parser.parse_args()
        
        file = args.get('file', None)
        text = args.get('text', None)
        
        task_args = {
            "voice_rate": args.get('voice_rate', None),
            "voice_id": args.get('voice_id', None),
            "voice_volume": args.get('voice_volume', None),
            "use_AI_method": args.get('use_AI', None)
        }
        
        file_save_path = None
        # and task_args.get('voice_id') is not None
        if text or file:
            
            if file and self.is_allowed(file.filename):
                
                # Save the file
                filename = secure_filename(file.filename)
                file_save_path = os.path.join(f"{app.config['UPLOAD_FOLDER']}/text", filename)
                file.save(file_save_path)
                
                # Create task for file
                task = text_to_voice_api_task.delay(
                    file_save_path=file_save_path,
                    **task_args
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
                    **task_args
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
