from sqlalchemy import Column, Integer, String
from models.base import Base
class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True,autoincrement=True,index=True)
    # 0:conference   1: journal
    flag = Column(Integer, index=False)
    description = Column(String, index=False)