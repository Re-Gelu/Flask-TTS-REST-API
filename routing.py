from app import api, app
import views

#app.add_url_rule("/uploads/audios/<filename>", endpoint="download_file", build_only=True)

api.add_resource(views.TextToVoiceAPIViewPOST, '/api/tts')
api.add_resource(views.TextToVoiceAPIViewGET, '/api/tts/<string:task_id>')
