from flask import send_from_directory
from flask_restful import Resource
from flask import request, render_template, url_for
from flask_restful import reqparse
import werkzeug
import pyttsx3
import os
from app import app
from app import celery
from app import cache
from app import limiter
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
    @limiter.limit("1000/hour;10000/day")
    def get(self, task_id: str):
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

    @limiter.limit("100/hour;1000/day")
    def delete(self, task_id):
        celery.control.revoke(task_id)
        return {
            "task_id": task_id,
            "is_deleted": True,
        }, 200


class TextToVoiceAPIView(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        
        self.parser.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        
        if request.is_json:
            self.parser.add_argument('text', type=str, location=['values', 'json'])
            self.parser.add_argument('voice_rate', type=int, location=['values', 'json'])
            self.parser.add_argument('voice_id', type=int, location=['values', 'json'])
            self.parser.add_argument('voice_volume', type=float, location=['values', 'json'])
            self.parser.add_argument('use_AI', type=bool, default=False, location=['values', 'json'])
        else:
            self.parser.add_argument('text', type=str, location='form')
            self.parser.add_argument('voice_rate', type=int, location='form')
            self.parser.add_argument('voice_id', type=int, location='form')
            self.parser.add_argument('voice_volume', type=float, location='form')
            self.parser.add_argument('use_AI', type=bool, default=False, location='form')

        super(TextToVoiceAPIView, self).__init__()

    @staticmethod
    def is_allowed(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config.get("ALLOWED_EXTENSIONS")

    @cache.cached()
    @limiter.limit("1000/hour;10000/day")
    def get(self):
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
        # Parse the file, text and other tts args from the post request
        args = self.parser.parse_args()

        print(args)

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
                #filename = secure_filename(file.filename)
                file_save_path = os.path.join(f"{app.config['UPLOAD_FOLDER']}\\text", file.filename)
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
