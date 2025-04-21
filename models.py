from sqlalchemy import Column, Integer, String
from database import Base

#creating a simple item model
class item(Base):
    __tablename__ = "items"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255), index=True)
    price = Column(Integer, index=True)