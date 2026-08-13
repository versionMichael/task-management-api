from fastapi import APIRouter, HTTPException, Depends
from app.database import SessionLocal
from app.models.user import User
from app.utils.security import verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):

    db = SessionLocal()

    user = db.query(User).filter(User.username==form_data.username).first()

    if not user:
        db.close()
        raise HTTPException(status_code=401, detail="Invalid username or password")

    if not verify_password(form_data.password, user.hashed_password):
        db.close()
        raise HTTPException(status_code=401, detail="Invalid username or password")

    db.close()

    access_token = create_access_token(data={"sub":str(user.id)})

    return {"access_token": access_token, "token_type": "bearer"}


