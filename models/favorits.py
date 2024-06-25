from sqlalchemy import Column, Integer, String
from models.base import Base

class Favorit(Base):
    __tablename__ = "favorits"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    