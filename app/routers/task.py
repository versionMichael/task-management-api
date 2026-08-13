from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app.models.task import Task
from app.schemas import TaskResponse, TaskCreate, UserResponse
from app.models.user import User
from app.utils.auth import get_current_user
from app.models.project import Project

router= APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/",response_model=list[TaskResponse])
def get_tasks(current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    tasks= (
        db.query(Task).join(Task.project).filter(Task.project.has(owner_id=current_user.id)).all())
    
    db.close()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int, current_user: User = Depends(get_current_user)):

    db = SessionLocal()

    task = db.query(Task).filter(Task.id== task_id).first()

    if not task: 
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    if task.project.owner_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this task"
        )

    db.close()

    return task


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    project = db.query(Project).filter(Project.id == task.project_id).first()

    if not project:
        db.close()
        raise HTTPException(status_code=404, detail="Project not found")

    if project.owner_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to create a task in this project"
        ) 

    new_task= Task(
        title=task.title,
        description=task.description,
        project_id= task.project_id,
        assigned_to= task.assigned_to
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    db.close()

    return new_task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, updated_task: TaskCreate, current_user : User = Depends(get_current_user)):

    db= SessionLocal()

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    if task.project.owner_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this task"
        )

    if updated_task.project_id!= task.project_id:
        new_project = db.query(Project).filter(Project.id==updated_task.project_id).first()

        if not new_project:
            db.close()
            raise HTTPException(
                status_code=404,
                detail="New project not found"
            )

        if new_project.owner_id != current_user.id:
            db.close()
            raise HTTPException(
                status_code=403,
                detail="Not authorized to move task to this project"
            )
            
    task.title = updated_task.title
    task.description = updated_task.description
    task.project_id = updated_task.project_id
    task.assigned_to = updated_task.assigned_to

    db.commit()
    db.refresh(task)

    db.close()
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    task = db.query(Task).filter(Task.id==task_id).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    if task.project.owner_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this task"
        )

    db.delete(task)
    db.commit()

    db.close()

    return {"message": "Task deleted successfully"}

@router.get("/{task_id}/user", response_model=UserResponse)
def get_task_user(task_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    if task.project.owner_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this task's user"
        )

    user = task.assignee

    db.close()

    return user