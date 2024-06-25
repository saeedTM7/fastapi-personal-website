# routers/skill.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models.skills import Skill

router = APIRouter()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new skill
@router.post("/skills/", response_model=dict)
def create_skill(skill_data: dict, db: Session = Depends(get_db)):
    skill = Skill(**skill_data)
    db.add(skill)
    db.commit()
    db.refresh(skill)
    return {"id": skill.id, "name": skill.name}

# Get an skill by ID
@router.get("/skills/{skill_id}", response_model=dict)
def get_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {"id": skill.id, "name": skill.name}

# Get all skills
@router.get("/skills/", response_model=list)
def list_skills(db: Session = Depends(get_db)):
    skills = db.query(Skill).all()
    return [{"id": skill.id, "name": skill.name} for skill in skills]

# Update an skill by ID
@router.put("/skills/{skill_id}", response_model=dict)
def update_skill(skill_id: int, update_data: dict, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    for key, value in update_data.skills():
        setattr(skill, key, value)

    db.commit()
    db.refresh(skill)

    return {"id": skill.id, "name": skill.name}

# Delete an skill by ID
@router.delete("/skills/{skill_id}", response_model=dict)
def delete_skill(skill_id: int, db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    
    db.delete(skill)
    db.commit()

    return {"message": f"Skill {skill_id} deleted successfully"}
