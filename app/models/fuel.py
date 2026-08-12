from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Fuel(Base):
    __tablename__ = "fuel"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=True)
    fuel_type = Column(String(50), nullable=False)
    quantity = Column(Float, nullable=False)
    price_per_litre = Column(Float, nullable=False)
    total_cost = Column(Float, nullable=False)
    fuel_date = Column(DateTime, nullable=False)
    vehicle = relationship("Vehicle", back_populates="fuel_records")
    trip = relationship("Trip", back_populates="fuel_records")
