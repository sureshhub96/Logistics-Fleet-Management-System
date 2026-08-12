from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional

class VehicleCreate(BaseModel):
    vehicle_number: str = Field(min_length=1, max_length=50)
    vehicle_type: str
    model: str
    manufacturing_year: int = Field(ge=1900, le=2100)
    capacity: float = Field(gt=0)
    current_km: float = Field(default=0, ge=0)
    status: Literal["Available", "Assigned", "Maintenance", "Inactive"] = "Available"

class VehicleUpdate(BaseModel):
    vehicle_type: Optional[str] = None
    model: Optional[str] = None
    manufacturing_year: Optional[int] = Field(default=None, ge=1900, le=2100)
    capacity: Optional[float] = Field(default=None, gt=0)
    current_km: Optional[float] = Field(default=None, ge=0)
    status: Optional[Literal["Available", "Assigned", "Maintenance", "Inactive"]] = None

class VehicleResponse(VehicleCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
