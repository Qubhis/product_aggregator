# Windows

### Navigate to the app folder and create virtual environment (venv)

```
python -m venv venv
```

### Activate virtual environment (venv)

```
venv\scripts\activate.bat
```

### Install dependencies

```
python -m pip install -r requirements.txt
```

### Create db file

```
python create_db.py
```

### Run celery worker:

```
celery -A app worker -f celery_worker.log --loglevel=info  --concurrency 1 -P solo
```

### Start Flask app:

```
python app.py
```

### Run celery scheduler:

```
celery -A app beat -f celery_beat.log --loglevel=info
```
