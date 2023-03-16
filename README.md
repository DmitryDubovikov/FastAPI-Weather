# FastAPI - Weather

## Project description:

This project is 1/2 test assignment and 1/2 pet project for skills development and demonstration.

User can add cities to DB to track its weather, fetch weather data for tracked cities from openweathermap, get weather stats and reports via API, email and in frontend.

## Technologies used: 
* FastAPI, 
* SQLAlchemy, 
* raw SQL queries,
* pydantic for validation,
* alembic for database migrations, 
* asyncpg for async queries to PostgreSQL, 
* fastapi_users for authentication, 
* docker, docker-compose for containerization,
* fastapi background_tasks for background_tasks,
* celery for background_tasks,
* flower for celery monitoring,
* Jinja2Templates and tailwindcss for frontend.

## Main api endpoints

### User registration and token generation endpoints

| Endpoint       | Method | Purpose                                    |
|----------------|--------|--------------------------------------------|
| /auth/register | POST   | Creates a new user with email and password |
| /auth/login    | POST   | Login and recieve JWT token                |
| /auth/logout   | POST   | Logout                                     |

### Weather endpoints

| Endpoint                | Method | Purpose                                                                                                     |
|-------------------------|--------|-------------------------------------------------------------------------------------------------------------|
| /weather/{city_name}    | POST   | Add city do DB to track its weather.                                                                        |
| /weather/last-weather/  | GET    | Get last saved in DB weather for each tracked city. Use optional 'search' parameter to filter among cities. |
| /weather/city-stats/    | GET    | For a given city (query paramater 'city_name') get all weather data and its average values.                 |
| /weather/fetch-weather/ | POST   | Fetch current weather from openweathermap for each tracked city.                                            |                                      |

## Other functions:

| Endpoint                        | Method | Purpose                                                        |
|---------------------------------|--------|----------------------------------------------------------------|
| /report/last-weather-background | GET    | Get last weather report email (using fastapi background tasks) |
| /report/last-weather-celery     | GET    | Get last weather report email (using celery tasks)             |
| /last-weather/                  |        | See last weather in browser                                    |

## How to run:

Run containers:

    docker-compose build
    docker-compose up

Run in docker:    

    alembic upgrade heads

Add your SMTP_PASSWORD, SMTP_USER and openweathermap API_KEY in .env file.

To auth:

    /auth/register - 200
    /auth/jwt/login - 200

Add some cities to track:

    curl -X 'POST' \
    'http://127.0.0.1:8000/weather/London' \
    -H 'accept: application/json' \
    -d ''

    curl -X 'POST' \
    'http://127.0.0.1:8000/weather/Buenos%20Aires' \
    -H 'accept: application/json' \
    -d ''

Fetch weather data for tracked cities from openweathermap for several times:

    curl -X 'POST' \
    'http://127.0.0.1:8000/weather/fetch-weather/' \
    -H 'accept: application/json' \
    -d ''

Try to get weather stats and reports via API, email and in frontend as described above.

![image](https://github.com/DmitryDubovikov/FastAPI/blob/main/browser.jpg)

Flower for celery task monitoring:

    http://127.0.0.1:8888/