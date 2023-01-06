from app import app
from app import celery
from TTS_module import TextToSpeech
from werkzeug.utils import secure_filename
import time
import os


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@celery.task(name="text_to_voice_api_task", bind=True)
def text_to_voice_api_task(self, file_save_path: str = None, text: str = None, file_save_name: str = None, 
                           voice_rate: int = None, voice_volume: float = None, voice_id: int = None, 
                           use_AI_method: bool = False, autoconvert_file: bool = True) -> str:

    tts_settings = {
        "file_save_name": secure_filename(f"{time.strftime('%d-%m-%Y %H-%M-%S')} Audio - {self.request.id}"),
        "save_path": os.path.join(f"{app.config.get('DOWNLOAD_FOLDER')}/audio/"),
        "voice_rate": voice_rate,
        "voice_volume": voice_volume,
        "voice_id": voice_id,
        "autoconvert_file": autoconvert_file,
        "driver_name": app.config.get('TTS_DRIVER_NAME'),
        "use_AI_method": use_AI_method,
        "AI_model_id": app.config.get('TTS_AI_MODEL_ID'),
        "use_AI_GPU": app.config.get('TTS_USE_AI_GPU')
    }
    
    try:
        if file_save_path:
            tts = TextToSpeech(
                file_path=file_save_path,
                **tts_settings
            )
            return tts.save()
        elif text:
            tts = TextToSpeech(
                text=text,
                **tts_settings
            )
            return tts.save()
        else:
            return "No file or text was provided!"
    except Exception as e:
        #return "Something went wrong..."
        return str(e)
