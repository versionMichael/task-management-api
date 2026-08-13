from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.task import Task
from app.schemas import TaskResponse, TaskCreate

router= APIRouter(
    prefix="/tasks",
    tags=["Tasks"]
)

@router.get("/",response_model=list[TaskResponse])
def get_tasks():
    db = SessionLocal()
    tasks= db.query(Task).all()
    db.close()
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):

    db = SessionLocal()

    task = db.query(Task).filter(Task.id== task_id).first()

    if not task: 
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    db.close()

    return task


@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate):
    db = SessionLocal()

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
def update_task(task_id: int, updated_task: TaskCreate):

    db= SessionLocal()

    task = db.query(Task).filter(Task.id == task_id).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    task.title = updated_task.title
    task.description = updated_task.description
    task.project_id = updated_task.project_id
    task.assigned_to = updated_task.assigned_to

    db.commit()
    db.refresh(task)

    db.close()
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int):
    db = SessionLocal()

    task = db.query(Task).filter(Task.id==task_id).first()

    if not task:
        db.close()
        raise HTTPException(status_code=404, detail="Task not found")

    db.delete(task)
    db.commit()

    db.close()

    return {"message": "Task deleted successfully"}