# :poop: Проект Text to Speech REST API на Flask
> Pet-проект. Создается в целях более лучшего изучения Flask :shipit:

## :triangular_ruler: Стек проекта: 
- Python 3.11 (Flask, Flask RESTful)
- HTML5, CSS (Bootstrap 5, UIkit), JS (jQuery)
- Celery, Redis

## :package: [Зависимости проекта](https://github.com/Re-Gelu/Text-to-Speech-API/blob/master/requirements.txt)

## :incoming_envelope: Celery

Очередь задач работает на Redis. После POST запроса с файлом или текстом создаётся TTS задача Celery с переданными параметрами. Результат задачи "живёт" N секунд и возвращается сериализируемым под json (параметры CELERY_RESULT_EXPIRE_TIME и TASK_SERIALIZER в настройках проекта)

- Команды 

```
  Windows:
$ celery -A app.celery worker --pool=solo --loglevel=info

  Linux:
$ celery -A app.celery worker --loglevel=info
```
