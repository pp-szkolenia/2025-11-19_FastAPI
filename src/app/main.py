from fastapi import FastAPI

from app.routers import tasks, users

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    title="Task manager API",
    description="Description of my API which is visible in the documentation",
    version="0.1.2"
)

app.include_router(tasks.router)
app.include_router(users.router)


@app.get("/", description="Test endpoint for demonstration purposes")
def root():
    return {"message": "Hello World!"}

