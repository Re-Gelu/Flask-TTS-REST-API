from .app import api
from . import views

api.add_resource(views.TaskRunnerView, '/api/tasks')
api.add_resource(views.TextToVoiceAPIView, '/api/tts')
