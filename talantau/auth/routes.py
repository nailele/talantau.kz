from fastapi import APIRouter, Depends, Form, HTTPException
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse

from talantau.auth.dependencies import get_current_user
from talantau.auth.jwt_handler import create_access_token
from talantau.config import BASE_DIR
from talantau.db.base import SessionLocal
from talantau.db.models import User as UserModel
from talantau.schemas.usercreate import UserCreate

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/register", response_class=HTMLResponse)
def get_register_page():
    with open(f"{BASE_DIR}/register.html", "r", encoding="utf-8") as f:
        return f.read()


@router.post("/register")
def register(email: str = Form(...), name: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    try:
        user_data = UserCreate(email=email, name=name, password=password).model_dump()
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=e.errors())

    db_user = db.query(UserModel).filter(user_data.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = UserModel(**user_data)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"User {email} registered"}

@router.post("/login")
def login(email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == email).first()
    if not db_user or not pwd_context.verify(password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(data={"sub": db_user.email})
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me")
def get_me(current_user: UserCreate = Depends(get_current_user)):
    return {"id": current_user.id, "email": current_user.email}