# routers/profile.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models.profile import Profile

router = APIRouter()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new profile
@router.post("/profiles/", response_model=dict)
def create_profile(profile_data: dict, db: Session = Depends(get_db)):
    profile = Profile(**profile_data)
    db.add(profile)
    db.commit()
    db.refresh(profile)
    return {"id": profile.id, "name": profile.name, "family": profile.family,"email": profile.email,"phone": profile.phone,"image": profile.image}

# Get an profile by ID
@router.get("/profiles/{profile_id}", response_model=dict)
def get_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return {"id": profile.id, "name": profile.name, "family": profile.family,"email": profile.email,"phone": profile.phone,"image": profile.image}

# Get all profiles
@router.get("/profiles/", response_model=list)
def list_profiles(db: Session = Depends(get_db)):
    profiles = db.query(Profile).all()
    return [{"id": profile.id, "name": profile.name, "family": profile.family,"email": profile.email,"phone": profile.phone,"image": profile.image} for profile in profiles]

# Update an profile by ID
@router.put("/profiles/{profile_id}", response_model=dict)
def update_profile(profile_id: int, update_data: dict, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    for key, value in update_data.profiles():
        setattr(profile, key, value)

    db.commit()
    db.refresh(profile)

    return {"id": profile.id, "name": profile.name, "family": profile.family,"email": profile.email,"phone": profile.phone,"image": profile.image}

# Delete an profile by ID
@router.delete("/profiles/{profile_id}", response_model=dict)
def delete_profile(profile_id: int, db: Session = Depends(get_db)):
    profile = db.query(Profile).filter(Profile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    db.delete(profile)
    db.commit()

    return {"message": f"Profile {profile_id} deleted successfully"}
