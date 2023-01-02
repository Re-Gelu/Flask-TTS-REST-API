from .app import app
from .app import celery
from .TTS import TextToSpeech
import time
import os


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@celery.task(name="text_to_voice_api_task")
def text_to_voice_api_task(file_save_path: str = None, text: str = None, voice_rate: int = None, voice_id: int = None, autoconvert_file: bool = True):
    tts_settings = {
        "save_path": os.path.join(f"{app.config['UPLOAD_FOLDER']}/audios/"),
        "voice_rate": voice_rate,
        "voice_id": voice_id,
        "autoconvert_file": autoconvert_file
    }
    if file_save_path:
        tts = TextToSpeech(
            file_path=file_save_path,
            **tts_settings
        )
    elif text:
        tts = TextToSpeech(
            text=text,
            **tts_settings
        )
    
    return tts.save()
