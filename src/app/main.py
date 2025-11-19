from fastapi import FastAPI

from app.routers import tasks, users

app = FastAPI()

app.include_router(tasks.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Hello World!"}

