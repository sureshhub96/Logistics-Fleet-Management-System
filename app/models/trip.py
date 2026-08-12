from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    driver_id = Column(Integer, ForeignKey("drivers.id"), nullable=False)
    source = Column(String(200), nullable=False)
    destination = Column(String(200), nullable=False)
    start_date = Column(DateTime, nullable=False)
    expected_delivery_date = Column(DateTime, nullable=False)
    distance = Column(Float, nullable=False)
    trip_status = Column(String(30), default="Scheduled", nullable=False)
    vehicle = relationship("Vehicle", back_populates="trips")
    driver = relationship("Driver", back_populates="trips")
    fuel_records = relationship("Fuel", back_populates="trip")
    tracking_records = relationship("Tracking", back_populates="trip")
