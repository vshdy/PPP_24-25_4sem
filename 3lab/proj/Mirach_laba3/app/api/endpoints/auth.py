from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from app.db.database import SessionLocal
from app.cruds.user import create_user, get_user_by_email
from app.models.user import User
from app.services.auth import create_token
from app.schemas.schemas import UserCreate, UserLogin, UserResponse
from fastapi import APIRouter, Depends
from app.services.auth import get_current_user
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=dict)
def register(user: UserCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="User already exists")
    create_user(db, user.email, user.password)
    return {"message": "User registered successfully"}

@router.post("/login", response_model=UserResponse, include_in_schema=True)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if not db_user or db_user.password != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(user.email)
    return {
        "id": db_user.id,
        "email": db_user.email,
        "token": token
    }

@router.get("/me")
def get_me(
    user=Depends(get_current_user),
    token: str = Depends(oauth2_scheme)
):
    return {
        "id": user["id"],
        "email": user["email"],
        "token": token
    }

@router.post("/token", include_in_schema=True)
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, form_data.username)
    if not db_user or db_user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_token(db_user.email)
    return {"access_token": token, "token_type": "bearer"}

