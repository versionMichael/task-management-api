from fastapi import FastAPI
from app.database import Base, engine

from app.models.user import User
from app.models.project import Project
from app.models.task import Task

from app.routers.user import router as user_router
from app.routers.project import router as project_router
from app.routers.task import router  as task_router
from app.routers.auth import router as auth_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Task Management API"}

app.include_router(user_router)
app.include_router(project_router)
app.include_router(task_router)
app.include_router(auth_router)