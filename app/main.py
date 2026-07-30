from fastapi import FastAPI
from app.database import Base, engine
from app.models.user import User
from app.models.project import Project

app = FastAPI()

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Task Management API"}