from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Vehicle(Base):
    __tablename__ = "vehicles"
    id = Column(Integer, primary_key=True)
    vehicle_number = Column(String(50), unique=True, nullable=False, index=True)
    vehicle_type = Column(String(50), nullable=False)
    model = Column(String(100), nullable=False)
    manufacturing_year = Column(Integer, nullable=False)
    capacity = Column(Float, nullable=False)
    current_km = Column(Float, default=0)
    status = Column(String(30), default="Available", nullable=False)
    trips = relationship("Trip", back_populates="vehicle")
    fuel_records = relationship("Fuel", back_populates="vehicle")
    maintenance_records = relationship("Maintenance", back_populates="vehicle")
