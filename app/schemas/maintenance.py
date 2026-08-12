from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from typing import Literal, Optional

class MaintenanceCreate(BaseModel):
    vehicle_id: int
    service_type: str
    service_date: datetime
    service_cost: float = Field(gt=0)
    current_km: float = Field(ge=0)
    description: Optional[str] = None
    status: Literal["Scheduled", "In Progress", "Completed"] = "Scheduled"

class MaintenanceUpdate(BaseModel):
    service_type: Optional[str] = None
    service_date: Optional[datetime] = None
    service_cost: Optional[float] = Field(default=None, gt=0)
    current_km: Optional[float] = Field(default=None, ge=0)
    description: Optional[str] = None
    status: Optional[Literal["Scheduled", "In Progress", "Completed"]] = None

class MaintenanceResponse(MaintenanceCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
