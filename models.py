from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,FLOAT,BigInteger
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "User"

    id = Column(String, primary_key=True, index=True)

    Fullname = Column(String)

    email = Column(String)

    password = Column(String)
    

class Rooms(Base):
    __tablename__="Rooms"

    id = Column(BigInteger, primary_key=True, index=True)
    room_id = Column(Integer)
    title = Column(String)
    long = Column(Integer)
    lat = Column(Integer)
    rating = Column(Integer)
    revenue = Column(Integer)
    room_type = Column(String)
    review = Column(Integer)
    bedroom = Column(Integer)
    bathroom = Column(Integer)
    days_available = Column(Integer)
    property_type = Column(String)