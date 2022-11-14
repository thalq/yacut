# YaCut
## Проект YaCut — это сервис укорачивания ссылок. 
Его назначение — ассоциировать длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.
## Ключевые возможности сервиса:
- генерация коротких ссылок и связь их с исходными длинными ссылками,
- переадресация на исходный адрес при обращении к коротким ссылкам.
## API для проекта
API проекта доступен всем желающим. Сервис обслуживает два эндпоинта:
- /api/id/ — POST-запрос на создание новой короткой ссылки;
- /api/id/<short_id>/ — GET-запрос на получение оригинальной ссылки по указанному короткому идентификатору.

Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:thalq/yacut.git
```

```
cd yacut
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/MacOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Запустить проект:

```
flask run
```

### Технологии:
- Python 3
- Flask 2.0
- REST API
- SQLAlchemy 1.4
- Git

### Автор:
Таня Халквист
