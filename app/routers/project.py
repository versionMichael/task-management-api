from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.project import Project
from app.schemas import ProjectResponse, ProjectCreate, TaskResponse

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.get("/", response_model=list[ProjectResponse])
def get_projects():
    db = SessionLocal()

    projects = db.query(Project).all()

    db.close()

    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id:int):
    db = SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    db.close()

    return project

@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate):
    db = SessionLocal()

    new_project = Project(
        name=project.name,
        description=project.description,
        owner_id=project.owner_id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    db.close()

    return new_project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, updated_project: ProjectCreate):

    db= SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    project.name= updated_project.name
    project.description = updated_project.description
    project.owner_id = updated_project.owner_id

    db.commit()
    db.refresh(project)

    db.close()

    return project

def delete_project(project_id: int):
    db = SessionLocal()

    project = db.query(Project).filter(Project.id==project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    db.delete(project)
    db.commit()

    db.close()

    return {"message" : "Project deleted successfully"}


@router.get("/{project_id}/tasks", response_model=list[TaskResponse])
def get_project_tasks(project_id: int):
    db = SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    tasks = project.tasks

    db.close()

    return tasks