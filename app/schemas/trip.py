from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional

class TripCreate(BaseModel):
    vehicle_id: int
    driver_id: int
    source: str
    destination: str
    start_date: datetime
    expected_delivery_date: datetime
    distance: float = Field(gt=0)

class TripResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    vehicle_id: int
    driver_id: int
    source: str
    destination: str
    start_date: datetime
    expected_delivery_date: datetime
    distance: float
    trip_status: str

class TrackingCreate(BaseModel):
    location: str
    status: Literal["Scheduled", "Started", "In Transit", "Delivered", "Cancelled"]
    remarks: Optional[str] = None

class TrackingResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    trip_id: int
    location: str
    status: str
    remarks: Optional[str]
    timestamp: datetime
