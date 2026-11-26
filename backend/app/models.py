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
    role = Column(String, default="student")
    face_encoding = Column(String, nullable=True)
    # Student registration fields
    enrollment_no = Column(String, nullable=True, index=True)
    section = Column(String, nullable=True)
    group = Column(String, nullable=True)   # G1 / G2

class Schedule(Base):
    __tablename__ = "schedules"

    id = Column(Integer, primary_key=True, index=True)
    course_name = Column(String, index=True)
    prof_id = Column(Integer, ForeignKey("users.id"))
    lat = Column(Float)
    lng = Column(Float)
    allowed_radius_m = Column(Float, default=50.0)
    full_name = Column(String, nullable=True)
    course_type = Column(String, default="theory")  # "theory" or "lab"
    room_or_lab = Column(String, nullable=True)
    faculty_name = Column(String, nullable=True)
    target_group = Column(String, nullable=True)    # "All", "G1", "G2"
    time_slot = Column(String, nullable=True)
    professor = relationship("User")

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("users.id"))
    schedule_id = Column(Integer, ForeignKey("schedules.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Present")
    student = relationship("User")
    schedule = relationship("Schedule")

class AttendanceSession(Base):
    """Tracks when a professor opens/closes attendance for a class."""
    __tablename__ = "attendance_sessions"

    id = Column(Integer, primary_key=True, index=True)
    schedule_id = Column(Integer, ForeignKey("schedules.id"))
    opened_by = Column(Integer, ForeignKey("users.id"))
    opened_at = Column(DateTime, default=datetime.utcnow)
    closed_at = Column(DateTime, nullable=True)
    is_active = Column(String, default="yes")

    schedule = relationship("Schedule")
    professor = relationship("User")
