from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class FuelCreate(BaseModel):
    vehicle_id: int
    trip_id: Optional[int] = None
    fuel_type: str
    quantity: float = Field(gt=0)
    price_per_litre: float = Field(gt=0)
    fuel_date: datetime

class FuelResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    vehicle_id: int
    trip_id: Optional[int]
    fuel_type: str
    quantity: float
    price_per_litre: float
    total_cost: float
    fuel_date: datetime
