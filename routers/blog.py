# routers/blog.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db import SessionLocal
from models.blog import Blog

router = APIRouter()

# Dependency to get a session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new blog
@router.post("/blogs/", response_model=dict)
def create_blog(blog_data: dict, db: Session = Depends(get_db)):
    blog = Blog(**blog_data)
    db.add(blog)
    db.commit()
    db.refresh(blog)
    return {"id": blog.id, "name": blog.name, "description": blog.description,"image": blog.image}

# Get an blog by ID
@router.get("/blogs/{blog_id}", response_model=dict)
def get_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    return {"id": blog.id, "name": blog.name, "description": blog.description,"image": blog.image}

# Get all blogs
@router.get("/blogs/", response_model=list)
def list_blogs(db: Session = Depends(get_db)):
    blogs = db.query(Blog).all()
    return [{"id": blog.id, "name": blog.name, "description": blog.description,"image": blog.image} for blog in blogs]

# Update an blog by ID
@router.put("/blogs/{blog_id}", response_model=dict)
def update_blog(blog_id: int, update_data: dict, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    for key, value in update_data.blogs():
        setattr(blog, key, value)

    db.commit()
    db.refresh(blog)

    return {"id": blog.id, "name": blog.name, "description": blog.description,"image": blog.image}

# Delete an blog by ID
@router.delete("/blogs/{blog_id}", response_model=dict)
def delete_blog(blog_id: int, db: Session = Depends(get_db)):
    blog = db.query(Blog).filter(Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")
    
    db.delete(blog)
    db.commit()

    return {"message": f"Blog {blog_id} deleted successfully"}
