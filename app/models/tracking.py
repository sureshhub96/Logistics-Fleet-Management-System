from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Tracking(Base):
    __tablename__ = "tracking"
    id = Column(Integer, primary_key=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    location = Column(String(200), nullable=False)
    status = Column(String(30), nullable=False)
    remarks = Column(Text, nullable=True)
    timestamp = Column(DateTime, nullable=False)
    trip = relationship("Trip", back_populates="tracking_records")
