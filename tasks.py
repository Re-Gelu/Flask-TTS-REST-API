from app import app
from app import celery
from TTS import TextToSpeech
import time
import os


@celery.task(name="create_task")
def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True


@celery.task(name="text_to_voice_api_task", bind=True)
def text_to_voice_api_task(self, file_save_path: str = None, text: str = None, file_save_name: str = None, voice_rate: int = None, voice_id: int = None, autoconvert_file: bool = True):
    
    tts_settings = {
        "file_save_name": self.request.id,
        "save_path": os.path.join(f"{app.config['UPLOAD_FOLDER']}/audios/"),
        "voice_rate": voice_rate,
        "voice_id": voice_id,
        "autoconvert_file": autoconvert_file
    }
    try:
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
    except Exception as e:
        return e
    
    return tts.save()
