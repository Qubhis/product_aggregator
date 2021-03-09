# Product aggregator microservice

Backend practice

## Requirements

Python 3.8

You must create ".env" file in the app folder prior to running this service. The file must contain:

```
OFFERS_BASE_URL="<offers_ms_api_point>"
FLASK_SECRET_KEY="<secret_key>"
JWT_SECRET_KEY="<secret_key>"
SQLALCHEMY_DB_URI="sqlite:///database.db"
```
When running locally:
```
CELERY_BROKER_URI="redis://localhost:6379/0"
```
Docker image
```
CELERY_BROKER_URI="redis://redis:6379/0"
```

## Linux install and run
Navigate to the app folder and create virtual environment (venv) - optional

```
python3 -m venv venv
```

Activate virtual environment (venv) - optional

```
source venv/bin/activate
```
Install Redis
```
sudo apt-get install redis-server
```
open redis client and set Redis user
```
redis-cli
 > set user:1 "Aggregator"
 > exit
```
Re-start Redis server
```
sudo service redis-server restart
```

Install dependencies

```
python3 -m pip install -r requirements.txt
```

Create db file

```
python3 create_db.py
```

Run celery worker:

```
celery -A app worker -f celery_worker.log --loglevel=info  --concurrency 1 -P solo
```

Start Flask app:

```
python3 app.py
```

Run celery scheduler:

```
celery -A app beat -f celery_beat.log --loglevel=info
```
## Docker
Componse and build
```
docker-compose up --build
```


## API documentation

Base URL (when run locally):

```
http://127.0.0.1:5000/api
```

### Getting access token - POST /auth

```
Headers: none
Request: none
Response:
201 CREATED
{
    "access_token": <jwt-token>
}
```

### Register product POST /products

```
Headers: Authorization: <jwt-token>
Request:
{
    "name": <product name>,
    "description": <product description>
}
Response:
201 CREATED
{
    "message": <message>,
    "id": <id stored in db>
}
400 BAD REQUEST
{
    "message": <message>
}
401 UNAUTHORIZED
{
    "msg": <message>
}
409 CONFLICT
{
    "message": <message>
}
```

### Update existing product PUT /product/<:id>

```
Headers: Authorization: <jwt-token>
Request: id of product in path
{
    "name": <product name>,
    "description": <product description>
}
Response:
200 OK
{
    "message": <message>
}
401 UNAUTHORIZED
{
    "msg": <message>
}
404 NOT FOUND
{
    "message": <message>
}
409 CONFLICT
{
    "message": <message>
}
```

### Delete existing product DELETE /product/<:id>

```
Headers: Authorization: <jwt-token>
Request: id of product in path
Response:
200 OK
{
    "message": <message>
}
401 UNAUTHORIZED
{
    "msg": <message>
}
404 NOT FOUND
{
    "message": <message>
}
```

### Get Price trends for last N minutes

### GET /product/<product_id>/offer/<offer_if>/trend/<:minutes>

```
Headers: Authorization: <jwt-token>
Request: product id, offer id, number of minutes provided in path
Response:
200 OK
{
    "offers": {"price": <price>, "timestamp": <datetime>},
    "percentage_increase": <price increase in percents>
}
401 UNAUTHORIZED
{
    "msg": <message>
}
404 NOT FOUND
{
    "message": <message>
}
```
