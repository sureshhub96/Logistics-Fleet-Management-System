from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    ConfigDict
)

from typing import Literal


class RegisterRequest(BaseModel):

    username: str = Field(
        min_length=3,
        max_length=100
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=72
    )

    role: Literal[
        "Admin",
        "Fleet Manager",
        "Driver"
    ] = "Driver"


class TokenResponse(BaseModel):

    access_token: str

    token_type: str


class UserResponse(BaseModel):

    model_config = ConfigDict(
        from_attributes=True
    )

    id: int

    username: str

    email: EmailStr

    role: str

    is_active: bool