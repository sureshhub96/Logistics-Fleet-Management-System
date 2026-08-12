from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Driver(Base):
    __tablename__ = "drivers"
    id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False, index=True)
    email = Column(String(255), nullable=False)
    phone = Column(String(30), nullable=False)
    license_number = Column(String(80), unique=True, nullable=False, index=True)
    license_expiry = Column(Date, nullable=False)
    experience = Column(Float, default=0)
    status = Column(String(30), default="Active", nullable=False)
    trips = relationship("Trip", back_populates="driver")
