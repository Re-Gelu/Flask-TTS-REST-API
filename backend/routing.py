from app import api
import views

api.add_resource(views.TextToVoiceAPIView, '/api/tts')
api.add_resource(views.TaskResultAPIView, '/api/tts/<string:task_id>')
