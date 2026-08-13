from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app.models.project import Project
from app.schemas import ProjectResponse, ProjectCreate, TaskResponse
from app.models.user import User
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/projects",
    tags=["Projects"]
)

@router.get("/", response_model=list[ProjectResponse])
def get_projects(current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    projects = db.query(Project).all()

    db.close()

    return projects

@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id:int, current_user: User= Depends(get_current_user)):
    db = SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        db.close()
        raise HTTPException(status_code=403, detail="Not authorized to access this project")

    db.close()

    return project

@router.post("/", response_model=ProjectResponse)
def create_project(project: ProjectCreate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    new_project = Project(
        name = project.name,
        description = project.description,
        owner_id = current_user.id
    )

    db.add(new_project)
    db.commit()
    db.refresh(new_project)

    db.close()

    return new_project

@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, updated_project: ProjectCreate, current_user: User=Depends(get_current_user)):

    db= SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this project"
        )

    project.name= updated_project.name
    project.description = updated_project.description

    db.commit()
    db.refresh(project)

    db.close()

    return project

@router.delete("/{project_id}")
def delete_project(project_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    project = db.query(Project).filter(Project.id==project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this project"
        )

    db.delete(project)
    db.commit()

    db.close()

    return {"message" : "Project deleted successfully"}


@router.get("/{project_id}/tasks", response_model=list[TaskResponse])
def get_project_tasks(project_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    project = db.query(Project).filter(Project.id == project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this project's tasks"
        )

    tasks = project.tasks

    db.close()

    return tasks