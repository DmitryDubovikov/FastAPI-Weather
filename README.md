# FastAPI

Run containers:

    docker-compose build
    docker-compose up

Run in docker:    

    alembic upgrade heads

Try auth:

    /unprotected-route - 200
    /protected-route - 401 

    /auth/register - 200
    /auth/jwt/login - 200
    /protected-route - 200