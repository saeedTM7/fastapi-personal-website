# models/profile.py
from sqlalchemy import Column, Integer, String
from models.base import Base

class Profile(Base):
    __tablename__ = "profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    family = Column(String, index=True)
    email = Column(String, index=True)
    phone = Column(String, index=True)
    image = Column(String, index=True)