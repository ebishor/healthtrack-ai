from typing import Literal

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    password: str = Field(min_length=12, max_length=128)
    role: Literal["clinician", "admin"] = "clinician"


class UserPublic(BaseModel):
    username: str
    role: Literal["clinician", "admin"]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"