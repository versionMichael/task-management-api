from fastapi import FastAPI
from app.database import Base, engine

from app.models.user import User
from app.models.project import Project
from app.models.task import Task

from app.routers.user import router as user_router

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Task Management API"}

app.include_router(user_router)