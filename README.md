# :poop: Проект Text to Speech REST API на Flask
> Pet-проект. Создается в целях более лучшего изучения Flask :shipit:

## :triangular_ruler: Стек проекта: 
- Python 3.9.12 (Flask, Flask RESTful, Celery)
- HTML5, CSS (Bootstrap 5, UIkit), JS (jQuery)
- Redis

## :package: [Зависимости проекта](https://github.com/Re-Gelu/Text-to-Speech-API/blob/master/requirements.txt)

## :whale: Работа с Docker

- Поднять контейнер (prod/dev - .env)
  ```
  $ docker-compose -f docker-compose.yml up -d --build
  ```
  
- Удаление контейнеров
  ```
  $ docker-compose down -v
  ```

## :incoming_envelope: Celery

Очередь задач работает на Redis. После POST запроса с файлом или текстом создаётся TTS задача Celery с переданными параметрами. Результат задачи "живёт" N секунд и возвращается сериализируемым под json (параметры CELERY_RESULT_EXPIRE_TIME и TASK_SERIALIZER в настройках проекта)

- Команды 

```
  Windows:
$ celery -A app.celery worker --pool=solo --loglevel=info

  Linux:
$ celery -A app.celery worker --loglevel=info
```

## work in progress...
