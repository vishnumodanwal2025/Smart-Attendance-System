from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# --- Token Schemas (For Login) ---
class Token(BaseModel):
    access_token: str
    token_type: str

# --- Simple login (email + password JSON body) ---
class SimpleLogin(BaseModel):
    email: str
    password: str

# --- User Schemas (For Registration & Profile) ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: str = "student"
    enrollment_no: Optional[str] = None
    section: Optional[str] = None
    group: Optional[str] = None   # G1 or G2

# This ensures we NEVER send the password back to the frontend
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    enrollment_no: Optional[str] = None
    section: Optional[str] = None
    group: Optional[str] = None

    class Config:
        from_attributes = True

# --- Schedule Schemas ---
class ScheduleCreate(BaseModel):
    course_name: str
    lat: float
    lng: float
    allowed_radius_m: float = 50.0
    full_name: Optional[str] = None
    course_type: Optional[str] = "theory"
    room_or_lab: Optional[str] = None
    faculty_name: Optional[str] = None
    target_group: Optional[str] = "All"
    time_slot: Optional[str] = None

class ScheduleResponse(ScheduleCreate):
    id: int
    prof_id: int

    class Config:
        from_attributes = True