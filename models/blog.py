# models/blog.py
from sqlalchemy import Column, Integer, String
from models.base import Base

class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    image = Column(String, index=True)