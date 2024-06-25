# routers/volunteer.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models.volunteers import Volunteer

router = APIRouter()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new volunteer
@router.post("/volunteers/", response_model=dict)
def create_volunteer(volunteer_data: dict, db: Session = Depends(get_db)):
    volunteer = Volunteer(**volunteer_data)
    db.add(volunteer)
    db.commit()
    db.refresh(volunteer)
    return {"id": volunteer.id, "name": volunteer.name}

# Get an volunteer by ID
@router.get("/volunteers/{volunteer_id}", response_model=dict)
def get_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    return {"id": volunteer.id, "name": volunteer.name}

# Get all volunteers
@router.get("/volunteers/", response_model=list)
def list_volunteers(db: Session = Depends(get_db)):
    volunteers = db.query(Volunteer).all()
    return [{"id": volunteer.id, "name": volunteer.name} for volunteer in volunteers]

# Update an volunteer by ID
@router.put("/volunteers/{volunteer_id}", response_model=dict)
def update_volunteer(volunteer_id: int, update_data: dict, db: Session = Depends(get_db)):
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    for key, value in update_data.volunteers():
        setattr(volunteer, key, value)

    db.commit()
    db.refresh(volunteer)

    return {"id": volunteer.id, "name": volunteer.name}

# Delete an volunteer by ID
@router.delete("/volunteers/{volunteer_id}", response_model=dict)
def delete_volunteer(volunteer_id: int, db: Session = Depends(get_db)):
    volunteer = db.query(Volunteer).filter(Volunteer.id == volunteer_id).first()
    if not volunteer:
        raise HTTPException(status_code=404, detail="Volunteer not found")
    
    db.delete(volunteer)
    db.commit()

    return {"message": f"Volunteer {volunteer_id} deleted successfully"}
