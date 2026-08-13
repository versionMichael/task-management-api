from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app.models.user import User
from app.schemas import UserCreate, UserResponse, ProjectResponse, TaskResponse, UserListResponse
from app.utils.security import hash_password
from app.utils.auth import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=list[UserListResponse])
def get_users(current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, current_user: User = Depends(get_current_user)):
    db = SessionLocal()

    user = db.query(User).filter(User.id== user_id).first()

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user"
        )

    db.close()

    return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    db = SessionLocal()

    new_user = User(
        username= user.username,
        email=user.email,
        hashed_password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return new_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserCreate, current_user : User=Depends(get_current_user)):
    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    if not user: 
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to update this user"
        )

    user.username = updated_user.username
    user.email = updated_user.email
    user.hashed_password = hash_password(updated_user.password)

    db.commit()
    db.refresh(user)

    db.close()

    return user

@router.delete("/{user_id}")
def delete_user(user_id: int, current_user : User = Depends(get_current_user)):
    db = SessionLocal()

    user = db.query(User).filter(User.id==user_id).first()

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to delete this user"
        )

    db.delete(user)
    db.commit()

    db.close()

    return {"message": "User deleted successfully"}


@router.get("/{user_id}/projects", response_model=list[ProjectResponse])
def get_user_projects(user_id: int, current_user : User = Depends(get_current_user)):
    db = SessionLocal()

    if user_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's projects"
        )

    user = db.query(User).filter(User.id==user_id).first()

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    projects = user.projects

    db.close()

    return projects

@router.get("/{user_id}/tasks", response_model=list[TaskResponse])
def get_user_tasks(user_id: int, current_user: User = Depends(get_current_user)):

    db= SessionLocal()

    if user_id != current_user.id:
        db.close()
        raise HTTPException(
            status_code=403,
            detail="Not authorized to access this user's tasks"
        )


    user= db.query(User).filter(User.id== user_id).first()

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    tasks = user.assigned_tasks

    db.close()

    return tasks