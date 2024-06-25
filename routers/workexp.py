# routers/workexp.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models.workexp import Workexp

router = APIRouter()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new workexp
@router.post("/workexps/", response_model=dict)
def create_workexp(workexp_data: dict, db: Session = Depends(get_db)):
    workexp = Workexp(**workexp_data)
    db.add(workexp)
    db.commit()
    db.refresh(workexp)
    return {"id": workexp.id, "name": workexp.name, "stDate": workexp.stDatee, "enDate": workexp.enDate,"site": workexp.site, "description": workexp.description}

# Get an workexp by ID
@router.get("/workexps/{workexp_id}", response_model=dict)
def get_workexp(workexp_id: int, db: Session = Depends(get_db)):
    workexp = db.query(Workexp).filter(Workexp.id == workexp_id).first()
    if not workexp:
        raise HTTPException(status_code=404, detail="Workexp not found")
    return {"id": workexp.id, "name": workexp.name, "stDate": workexp.stDatee, "enDate": workexp.enDate,"site": workexp.site, "description": workexp.description}

# Get all workexps
@router.get("/workexps/", response_model=list)
def list_workexps(db: Session = Depends(get_db)):
    workexps = db.query(Workexp).all()
    return [{"id": workexp.id, "name": workexp.name, "stDate": workexp.stDatee, "enDate": workexp.enDate,"site": workexp.site, "description": workexp.description} for workexp in workexps]

# Update an workexp by ID
@router.put("/workexps/{workexp_id}", response_model=dict)
def update_workexp(workexp_id: int, update_data: dict, db: Session = Depends(get_db)):
    workexp = db.query(Workexp).filter(Workexp.id == workexp_id).first()
    if not workexp:
        raise HTTPException(status_code=404, detail="Workexp not found")
    
    for key, value in update_data.workexps():
        setattr(workexp, key, value)

    db.commit()
    db.refresh(workexp)

    return {"id": workexp.id, "name": workexp.name, "stDate": workexp.stDatee, "enDate": workexp.enDate,"site": workexp.site, "description": workexp.description}

# Delete an workexp by ID
@router.delete("/workexps/{workexp_id}", response_model=dict)
def delete_workexp(workexp_id: int, db: Session = Depends(get_db)):
    workexp = db.query(Workexp).filter(Workexp.id == workexp_id).first()
    if not workexp:
        raise HTTPException(status_code=404, detail="Workexp not found")
    
    db.delete(workexp)
    db.commit()

    return {"message": f"Workexp {workexp_id} deleted successfully"}