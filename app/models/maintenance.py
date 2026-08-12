from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Maintenance(Base):
    __tablename__ = "maintenance"
    id = Column(Integer, primary_key=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    service_type = Column(String(100), nullable=False)
    service_date = Column(DateTime, nullable=False)
    service_cost = Column(Float, nullable=False)
    current_km = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(30), default="Scheduled", nullable=False)
    vehicle = relationship("Vehicle", back_populates="maintenance_records")
