# routers/lesson.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models.lessons import Lesson

router = APIRouter()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new lesson
@router.post("/lessons/", response_model=dict)
def create_lesson(lesson_data: dict, db: Session = Depends(get_db)):
    lesson = Lesson(**lesson_data)
    db.add(lesson)
    db.commit()
    db.refresh(lesson)
    return {"id": lesson.id, "name": lesson.name}

# Get an lesson by ID
@router.get("/lessons/{lesson_id}", response_model=dict)
def get_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    return {"id": lesson.id, "name": lesson.name}

# Get all lessons
@router.get("/lessons/", response_model=list)
def list_lessons(db: Session = Depends(get_db)):
    lessons = db.query(Lesson).all()
    return [{"id": lesson.id, "name": lesson.name} for lesson in lessons]

# Update an lesson by ID
@router.put("/lessons/{lesson_id}", response_model=dict)
def update_lesson(lesson_id: int, update_data: dict, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    for key, value in update_data.lessons():
        setattr(lesson, key, value)

    db.commit()
    db.refresh(lesson)

    return {"id": lesson.id, "name": lesson.name}

# Delete an lesson by ID
@router.delete("/lessons/{lesson_id}", response_model=dict)
def delete_lesson(lesson_id: int, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    db.delete(lesson)
    db.commit()

    return {"message": f"Lesson {lesson_id} deleted successfully"}
