from sqlalchemy import Column, Integer, String
from models.base import Base

class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)    