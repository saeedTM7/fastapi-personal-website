from sqlalchemy import Column, Integer, String
from models.base import Base

class Workexp(Base):
    __tablename__ = "workexps"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    stDate = Column(String, index=True)
    enDate = Column(String, index=True)
    site = Column(String, index=True)
    description = Column(String, index=True)    