from sqlalchemy import Column, Integer, String
from database import Base 

class Order(Base):
    __tablename__  = "orders"

    id = Column(Integer, primary_key=True)
    stripe_session_id = Column(String, unique=True)
    status = Column(String)
