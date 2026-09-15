from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=12, max_length=128)
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    organization_name: str = Field(min_length=1, max_length=255)


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    first_name: str
    last_name: str
