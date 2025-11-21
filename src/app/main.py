import time
from fastapi import FastAPI, Request

from app.routers import tasks, users, auth
from app.middleware import confirm_deletion, log_operations

app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    title="Task manager API",
    description="Description of my API which is visible in the documentation",
    version="0.1.2"
)

app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/", description="Test endpoint for demonstration purposes")
def root():
    return {"message": "Hello World!"}


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    process_time = end_time - start_time

    response.headers["X-Process-Time"] = str(process_time)
    return response

app.middleware("http")(log_operations)
