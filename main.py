import uvicorn
from fastapi import FastAPI

app = FastAPI(title="My FastAPI App")


@app.get("/")
async def hello():
    return {"message": "Hello World!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
