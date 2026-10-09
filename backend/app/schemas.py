from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- Token Schemas (For Login) ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- User Schemas (For Registration & Profile) ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str  # e.g., "student" or "professor"

# This ensures we NEVER send the password back to the frontend
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str

    class Config:
        from_attributes = True

# --- Schedule Schemas ---
class ScheduleCreate(BaseModel):
    course_name: str
    lat: float
    lng: float
    allowed_radius_m: float = 50.0

class ScheduleResponse(ScheduleCreate):
    id: int
    prof_id: int

    class Config:
        from_attributes = True