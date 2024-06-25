# routers/publication.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models.publications import Publication

router = APIRouter()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new publication
@router.post("/publications/", response_model=dict)
def create_publication(publication_data: dict, db: Session = Depends(get_db)):
    publication = Publication(flag=publication_data.get("flag"), description=publication_data.get("description"))
    db.add(publication)
    db.commit()
    db.refresh(publication)
    return {"id": publication.id,"flag": publication.flag,"description": publication.description}

# Get an publication by ID
@router.get("/publications/{publication_id}", response_model=dict)
def get_publication(publication_id: int, db: Session = Depends(get_db)):
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    return {"id": publication.id,"flag": publication.flag,"description": publication.description}

# Get all publications
@router.get("/publications/", response_model=list)
def list_publications(db: Session = Depends(get_db)):
    publications = db.query(Publication).all()
    return [{"id": publication.id,"flag": publication.flag,"description": publication.description} for publication in publications]

# Update an publication by ID
@router.put("/publications/{publication_id}", response_model=dict)
def update_publication(publication_id: int, update_data: dict, db: Session = Depends(get_db)):
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    
    for key, value in update_data.publications():
        setattr(publication, key, value)

    db.commit()
    db.refresh(publication)

    return {"id": publication.id, "name": publication.name,"stDate": publication.stDate,"jcname": publication.jcname, "description": publication.description}

# Delete an publication by ID
@router.delete("/publications/{publication_id}", response_model=dict)
def delete_publication(publication_id: int, db: Session = Depends(get_db)):
    publication = db.query(Publication).filter(Publication.id == publication_id).first()
    if not publication:
        raise HTTPException(status_code=404, detail="Publication not found")
    
    db.delete(publication)
    db.commit()

    return {"message": f"Publication {publication_id} deleted successfully"}
