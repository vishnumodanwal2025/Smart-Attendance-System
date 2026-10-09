from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)  # We will use "student" or "professor"
    face_encoding = Column(String, nullable=True) # Stores reference image path

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, index=True)
    prof_id = Column(Integer, ForeignKey("users.id"))
    
    # Geofencing coordinates (where the class is held)
    lat = Column(Float)
    lng = Column(Float)
    allowed_radius_m = Column(Float, default=50.0) # Must be within 50 meters
    
    # Links back to the User (Professor)
    professor = relationship("User")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    schedule_id = Column(Integer, ForeignKey("schedules.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Present")
    
    # Links to User and Schedule
    student = relationship("User")
    schedule = relationship("Schedule")