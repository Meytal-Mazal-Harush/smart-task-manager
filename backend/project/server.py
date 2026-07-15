from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import logging

from project.api.user_router import router as user_router
from project.api.task_router import router as task_router
from project.api.project_router import router as project_router
from project.api.comment_router import router as comment_router
from project.dal.db_context import init_db

logging.basicConfig(
    filename="server.log",
    level=logging.INFO,
    format="%(message)s"
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Smart Task Manager API",
    description="מערכת מתקדמת לניהול משימות וצוותים",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    log_line = f"{datetime.now()} | {request.method} {request.url.path} | status={response.status_code}"
    logging.info(log_line)
    return response


app.include_router(user_router)
app.include_router(task_router)
app.include_router(project_router)
app.include_router(comment_router)


@app.get("/", tags=["Root"])
def root():
    return {"status": "Server is running!", "database": "SQLite Local"}
