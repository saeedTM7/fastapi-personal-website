# routers/education.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models.education import Education

router = APIRouter()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new education
@router.post("/educations/", response_model=dict)
def create_education(education_data: dict, db: Session = Depends(get_db)):
    education = Education(**education_data)
    db.add(education)
    db.commit()
    db.refresh(education)
    return {"id": education.id, "name": education.name, "stDate": education.stDate, "enDate": education.enDate, "description": education.description}

# Get an education by ID
@router.get("/educations/{education_id}", response_model=dict)
def get_education(education_id: int, db: Session = Depends(get_db)):
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    return {"id": education.id, "name": education.name, "stDate": education.stDate, "enDate": education.enDate, "description": education.description}

# Get all educations
@router.get("/educations/", response_model=list)
def list_educations(db: Session = Depends(get_db)):
    educations = db.query(Education).all()
    return [{"id": education.id, "name": education.name, "stDate": education.stDate, "enDate": education.enDate, "description": education.description} for education in educations]

# Update an education by ID
@router.put("/educations/{education_id}", response_model=dict)
def update_education(education_id: int, update_data: dict, db: Session = Depends(get_db)):
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    
    for key, value in update_data.educations():
        setattr(education, key, value)

    db.commit()
    db.refresh(education)

    return {"id": education.id, "name": education.name, "stDate": education.stDate, "enDate": education.enDate, "description": education.description}

# Delete an education by ID
@router.delete("/educations/{education_id}", response_model=dict)
def delete_education(education_id: int, db: Session = Depends(get_db)):
    education = db.query(Education).filter(Education.id == education_id).first()
    if not education:
        raise HTTPException(status_code=404, detail="Education not found")
    
    db.delete(education)
    db.commit()

    return {"message": f"Education {education_id} deleted successfully"}
