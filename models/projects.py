from sqlalchemy import Column, Integer, String
from models.base import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    link = Column(String, index=True)
    description = Column(String, index=True)
    