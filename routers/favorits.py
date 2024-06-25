# routers/favorit.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models.favorits import Favorit

router = APIRouter()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new favorit
@router.post("/favorits/", response_model=dict)
def create_favorit(favorit_data: dict, db: Session = Depends(get_db)):
    favorit = Favorit(**favorit_data)
    db.add(favorit)
    db.commit()
    db.refresh(favorit)
    return {"id": favorit.id, "name": favorit.name}

# Get an favorit by ID
@router.get("/favorits/{favorit_id}", response_model=dict)
def get_favorit(favorit_id: int, db: Session = Depends(get_db)):
    favorit = db.query(Favorit).filter(Favorit.id == favorit_id).first()
    if not favorit:
        raise HTTPException(status_code=404, detail="Favorit not found")
    return {"id": favorit.id, "name": favorit.name}

# Get all favorits
@router.get("/favorits/", response_model=list)
def list_favorits(db: Session = Depends(get_db)):
    favorits = db.query(Favorit).all()
    return [{"id": favorit.id, "name": favorit.name} for favorit in favorits]

# Update an favorit by ID
@router.put("/favorits/{favorit_id}", response_model=dict)
def update_favorit(favorit_id: int, update_data: dict, db: Session = Depends(get_db)):
    favorit = db.query(Favorit).filter(Favorit.id == favorit_id).first()
    if not favorit:
        raise HTTPException(status_code=404, detail="Favorit not found")
    
    for key, value in update_data.favorits():
        setattr(favorit, key, value)

    db.commit()
    db.refresh(favorit)

    return {"id": favorit.id, "name": favorit.name}

# Delete an favorit by ID
@router.delete("/favorits/{favorit_id}", response_model=dict)
def delete_favorit(favorit_id: int, db: Session = Depends(get_db)):
    favorit = db.query(Favorit).filter(Favorit.id == favorit_id).first()
    if not favorit:
        raise HTTPException(status_code=404, detail="Favorit not found")
    
    db.delete(favorit)
    db.commit()

    return {"message": f"Favorit {favorit_id} deleted successfully"}
