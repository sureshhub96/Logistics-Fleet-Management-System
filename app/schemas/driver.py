from datetime import date
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Literal, Optional

class DriverCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    phone: str = Field(min_length=7, max_length=30)
    license_number: str = Field(min_length=2, max_length=80)
    license_expiry: date
    experience: float = Field(default=0, ge=0)
    status: Literal["Active", "Inactive"] = "Active"

class DriverUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    license_expiry: Optional[date] = None
    experience: Optional[float] = Field(default=None, ge=0)
    status: Optional[Literal["Active", "Inactive"]] = None

class DriverResponse(DriverCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
