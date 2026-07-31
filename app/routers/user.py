from fastapi import APIRouter, HTTPException
from app.database import SessionLocal
from app.models.user import User
from app.schemas import UserCreate, UserResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_model=list[UserResponse])
def get_users():
    db = SessionLocal()

    users = db.query(User).all()

    db.close()

    return users

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    db = SessionLocal()

    user = db.query(User).filter(User.id== user_id).first()

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    db.close()

    return user

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate):
    db = SessionLocal()

    new_user = User(
        username= user.username,
        email=user.email,
        hashed_password=user.password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    db.close()

    return new_user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(user_id: int, updated_user: UserCreate):
    db = SessionLocal()

    user = db.query(User).filter(User.id == user_id).first()

    if not user: 
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    user.username = updated_user.username
    user.email = updated_user.email
    user.hashed_password = updated_user.password

    db.commit()
    db.refresh(User)

    db.close()

    return user

router.delete("/{user_id}")
def delete_user(user_id: int):
    db = SessionLocal()

    user = db.query(User).filter(User.id==user_id).first()

    if not user:
        db.close()
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()

    db.close()

    return {"Message": "User deleted successfully"}