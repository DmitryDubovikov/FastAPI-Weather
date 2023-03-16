# FastAPI

## Описание проекта:

тут описание проекта

Используемые технологии: 
* FastAPI, 
* SQLAlchemy, 
* raw sql,
* pydantic для валидации,
* alembic для миграций, 
* asyncpg для асинхронных запросов в PostgreSQL, 
* fastapi_users для аутентификации, 
* Docker, Docker-compose,
* fastapi background_tasks,
* Celery,
* flower,
* Jinja2Templates,
* tailwindcss.

## Инструкция по развёртыванию:

Run containers:

    docker-compose build
    docker-compose up

Run in docker:    

    alembic upgrade heads

Add your SMTP_PASSWORD, SMTP_USER in .env to use email sending.

Try auth:

    /unprotected-route - 200
    /protected-route - 401 

    /auth/register - 200
    /auth/jwt/login - 200
    /protected-route - 200

Add cities:

    curl -X 'POST' \
    'http://127.0.0.1:8000/weather/London' \
    -H 'accept: application/json' \
    -d ''

    curl -X 'POST' \
    'http://127.0.0.1:8000/weather/Paris' \
    -H 'accept: application/json' \
    -d ''

    curl -X 'POST' \
    'http://127.0.0.1:8000/weather/Buenos%20Aires' \
    -H 'accept: application/json' \
    -d ''

Add weather data:

    curl -X 'POST' \
    'http://127.0.0.1:8000/weather/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "city_id": 1,
    "temperature": 2.6,
    "pressure": 760,
    "wind": 3
    }'

    curl -X 'POST' \
    'http://127.0.0.1:8000/weather/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "city_id": 1,
    "temperature": 2.8,
    "pressure": 762,
    "wind": 4
    }'

    curl -X 'POST' \
    'http://127.0.0.1:8000/weather/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "city_id": 2,
    "temperature": 4.0,
    "pressure": 764,
    "wind": 0
    }'

    curl -X 'POST' \
    'http://127.0.0.1:8000/weather/' \
    -H 'accept: application/json' \
    -H 'Content-Type: application/json' \
    -d '{
    "city_id": 2,
    "temperature": 5.0,
    "pressure": 766,
    "wind": 2
    }'

Flower monitoring:

    http://127.0.0.1:8888/