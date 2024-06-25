from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from middleware import auth
from db import SessionLocal
from models.users import User
from pydantic import BaseModel



router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class UserCreate(BaseModel):
    username: str
    password: str

class LoginData(BaseModel):
    username: str
    password: str

@router.post("/register/", response_model=dict) 
def register_user(user_data: UserCreate, db: Session = Depends(get_db)): 
    username = user_data.username  
    password = user_data.password

    db_user = auth.get_user(db, username=username)  
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    new_user = auth.create_user(db, username=username, password=password)  

    return {"message": "User created successfully", "user_id": new_user.id}

@router.get("/users/", response_model=list)
def list_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [{"id": user.id, "name": user.username} for user in users]

@router.post("/login/")
def login(user_data: LoginData, db: Session = Depends(get_db)):  # Use the schema
    username = user_data.username
    password = user_data.password
    
    user = auth.get_user(db, username)  # Ensure 'get_user' works as expected
    if not user or not auth.verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    
    access_token = auth.create_access_token(data={"sub": user.username})  # Create an access token
    return {"access_token": access_token, "token_type": "bearer"}

