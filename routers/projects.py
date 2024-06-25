# routers/project.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models.projects import Project

router = APIRouter()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new project
@router.post("/projects/", response_model=dict)
def create_project(project_data: dict, db: Session = Depends(get_db)):
    project = Project(**project_data)
    db.add(project)
    db.commit()
    db.refresh(project)
    return {"id": project.id, "name": project.name, "description": project.description,"link": project.link }

# Get an project by ID
@router.get("/projects/{project_id}", response_model=dict)
def get_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return {"id": project.id, "name": project.name, "description": project.description,"link": project.link}

# Get all projects
@router.get("/projects/", response_model=list)
def list_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()
    return [{"id": project.id, "name": project.name, "description": project.description,"link": project.link} for project in projects]

# Update an project by ID
@router.put("/projects/{project_id}", response_model=dict)
def update_project(project_id: int, update_data: dict, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    for key, value in update_data.projects():
        setattr(project, key, value)

    db.commit()
    db.refresh(project)

    return {"id": project.id, "name": project.name, "description": project.description,"link": project.link}

# Delete an project by ID
@router.delete("/projects/{project_id}", response_model=dict)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(project)
    db.commit()

    return {"message": f"Project {project_id} deleted successfully"}
