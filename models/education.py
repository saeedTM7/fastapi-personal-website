from sqlalchemy import Column, Integer, String
from models.base import Base

class Education(Base):
    __tablename__ = "educations"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=False)
    stDate = Column(String, index=False)
    enDate = Column(String, index=False)
    description = Column(String, index=False)
    