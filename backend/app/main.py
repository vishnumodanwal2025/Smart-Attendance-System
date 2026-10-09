from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas, auth
from .database import engine, get_db, SessionLocal
import math
import shutil
import os
import cv2
import numpy as np

# Automatically create tables in Supabase or SQLite if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="College Attendance AI System")

# --- CORS Middleware Setup (Must be right after app initialization) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods
    allow_headers=["*"],  # Allows all headers
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Setup directories for static face uploads
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "faces")
FRONTEND_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "frontend", "index.html"))
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.on_event("startup")
def init_db_data():
    """Seed initial sample data if tables are empty for immediate out-of-the-box demo."""
    db = SessionLocal()
    try:
        if db.query(models.User).count() == 0:
            user1_path = os.path.join(UPLOAD_DIR, "user_1.jpg")
            user2_path = os.path.join(UPLOAD_DIR, "user_2.jpg")

            user1 = models.User(
                name="Alex Johnson",
                email="student@college.edu",
                hashed_password=auth.get_password_hash("student123"),
                role="student",
                face_encoding=user1_path if os.path.exists(user1_path) else None
            )
            user2 = models.User(
                name="Dr. Alan Turing",
                email="prof@college.edu",
                hashed_password=auth.get_password_hash("prof123"),
                role="professor",
                face_encoding=user2_path if os.path.exists(user2_path) else None
            )
            db.add_all([user1, user2])
            db.commit()
            db.refresh(user1)
            db.refresh(user2)

            schedule1 = models.Schedule(
                course_name="CS101: Artificial Intelligence & Computer Vision",
                lat=27.646560,
                lng=77.551925,
                allowed_radius_m=1000.0,
                prof_id=user2.id
            )
            db.add(schedule1)
            db.commit()
            print("[DB Seed] Seeded default student (ID 1), professor (ID 2), and CS101 schedule (ID 1).")
    except Exception as e:
        print(f"[DB Seed Error] {e}")
    finally:
        db.close()

def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the earth in meters
    R = 6371000 
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = math.sin(delta_phi / 2.0) ** 2 + \
        math.cos(phi1) * math.cos(phi2) * \
        math.sin(delta_lambda / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c # Distance in meters

@app.api_route("/", methods=["GET", "HEAD"], response_class=HTMLResponse)
def read_root():
    if os.path.exists(FRONTEND_FILE):
        with open(FRONTEND_FILE, "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    return HTMLResponse(content="<h1>College Attendance AI System is Live!</h1><p><a href='/docs'>Swagger API Docs</a></p>")

@app.api_route("/api/health", methods=["GET", "HEAD"])
def api_health():
    return {"status": "success", "message": "The Attendance API is live!"}

# --- User Registration Route ---
@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email is already registered"
        )
    
    hashed_pwd = auth.get_password_hash(user.password)
    
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- User Login Route ---
@app.post("/login", response_model=schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# --- Create a Schedule (Professor Only) ---
@app.post("/schedules", response_model=schemas.ScheduleResponse, status_code=status.HTTP_201_CREATED)
def create_schedule(schedule: schemas.ScheduleCreate, current_user_id: int = 1, db: Session = Depends(get_db)):
    new_schedule = models.Schedule(
        course_name=schedule.course_name,
        lat=schedule.lat,
        lng=schedule.lng,
        allowed_radius_m=schedule.allowed_radius_m,
        prof_id=current_user_id
    )
    
    db.add(new_schedule)
    db.commit()
    db.refresh(new_schedule)
    return new_schedule

# --- Get All Schedules ---
@app.get("/schedules", response_model=list[schemas.ScheduleResponse])
def get_schedules(db: Session = Depends(get_db)):
    schedules = db.query(models.Schedule).all()
    return schedules

class AttendanceCheckIn(schemas.BaseModel):
    student_id: int
    schedule_id: int
    lat: float
    lng: float

@app.post("/attendance/check-in", status_code=status.HTTP_201_CREATED)
def mark_attendance(data: AttendanceCheckIn, db: Session = Depends(get_db)):
    schedule = db.query(models.Schedule).filter(models.Schedule.id == data.schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")
    
    distance = calculate_distance(data.lat, data.lng, schedule.lat, schedule.lng)
    
    if distance > schedule.allowed_radius_m:
        raise HTTPException(
            status_code=400, 
            detail=f"Geofencing failed! You are {round(distance, 2)} meters away. Must be within {schedule.allowed_radius_m} meters."
        )
    
    new_attendance = models.Attendance(
        student_id=data.student_id,
        schedule_id=data.schedule_id,
        status="Present"
    )
    db.add(new_attendance)
    db.commit()
    db.refresh(new_attendance)
    
    return {
        "status": "success",
        "message": "Attendance marked successfully!",
        "distance_meters": round(distance, 2)
    }

# --- Upload Face Reference Route ---
@app.post("/users/{user_id}/upload-face", status_code=status.HTTP_200_OK)
async def upload_face(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user:
            return {"status": "error", "message": "User not found"}
        
        file_path = os.path.join(UPLOAD_DIR, f"user_{user_id}.jpg")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        user.face_encoding = file_path
        db.commit()
        
        return {
            "status": "success",
            "message": "Face reference image uploaded successfully!",
            "file_path": file_path
        }
    except Exception as e:
        return {"status": "error", "message": str(e)}

# --- OpenCV Face Verification Route ---
@app.post("/attendance/verify-face/{user_id}")
async def verify_student_face(user_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.id == user_id).first()
        if not user or not user.face_encoding:
            return {"status": "error", "message": "User or baseline face reference not found"}
        
        reference_image_path = user.face_encoding
        if not os.path.exists(reference_image_path):
            return {"status": "error", "message": f"Reference image file not found on disk: {reference_image_path}"}
        
        temp_selfie_path = os.path.join(UPLOAD_DIR, f"temp_{user_id}.jpg")
        with open(temp_selfie_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        img_ref = cv2.imread(reference_image_path)
        img_live = cv2.imread(temp_selfie_path)
        
        if img_ref is None or img_live is None:
            if os.path.exists(temp_selfie_path):
                os.remove(temp_selfie_path)
            return {"status": "error", "message": "Could not decode image files using OpenCV."}
            
        img_ref_resized = cv2.resize(img_ref, (200, 200))
        img_live_resized = cv2.resize(img_live, (200, 200))
        
        hist_ref = cv2.calcHist([img_ref_resized], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist_live = cv2.calcHist([img_live_resized], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        
        cv2.normalize(hist_ref, hist_ref)
        cv2.normalize(hist_live, hist_live)
        
        similarity = cv2.compareHist(hist_ref, hist_live, cv2.HISTCMP_CORREL)
        
        if os.path.exists(temp_selfie_path):
            os.remove(temp_selfie_path)
            
        MATCH_THRESHOLD = 0.40
        is_verified = bool(similarity >= MATCH_THRESHOLD)
        
        return {
            "status": "success" if is_verified else "failed",
            "message": "Face verified successfully!" if is_verified else "Face verification failed! Similarity too low.",
            "verified": is_verified,
            "similarity_score": round(float(similarity), 2)
        }
        
    except Exception as e:
        if 'temp_selfie_path' in locals() and os.path.exists(temp_selfie_path):
            os.remove(temp_selfie_path)
        return {"status": "error", "message": str(e)}

# --- Unified Check-In Route (Geofencing + Face Verification) ---
@app.post("/attendance/unified-check-in", status_code=status.HTTP_201_CREATED)
async def unified_check_in(
    student_id: int,
    schedule_id: int,
    lat: float,
    lng: float,
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    try:
        user = db.query(models.User).filter(models.User.id == student_id).first()
        if not user or not user.face_encoding:
            return {"status": "error", "message": "Student or baseline face reference not found"}
        
        reference_image_path = user.face_encoding
        if not os.path.exists(reference_image_path):
            return {"status": "error", "message": "Reference face image missing on server disk"}

        schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
        if not schedule:
            return {"status": "error", "message": "Schedule not found"}
        
        distance = calculate_distance(lat, lng, schedule.lat, schedule.lng)
        if distance > schedule.allowed_radius_m:
            return {
                "status": "failed",
                "message": f"Geofencing failed! You are {round(distance, 2)} meters away. Must be within {schedule.allowed_radius_m} meters.",
                "distance_meters": round(distance, 2)
            }

        temp_selfie_path = os.path.join(UPLOAD_DIR, f"temp_checkin_{student_id}.jpg")
        with open(temp_selfie_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        img_ref = cv2.imread(reference_image_path)
        img_live = cv2.imread(temp_selfie_path)
        
        if img_ref is None or img_live is None:
            if os.path.exists(temp_selfie_path):
                os.remove(temp_selfie_path)
            return {"status": "error", "message": "Could not decode uploaded selfie image."}
            
        img_ref_resized = cv2.resize(img_ref, (200, 200))
        img_live_resized = cv2.resize(img_live, (200, 200))
        
        hist_ref = cv2.calcHist([img_ref_resized], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist_live = cv2.calcHist([img_live_resized], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        
        cv2.normalize(hist_ref, hist_ref)
        cv2.normalize(hist_live, hist_live)
        
        similarity = cv2.compareHist(hist_ref, hist_live, cv2.HISTCMP_CORREL)
        
        if os.path.exists(temp_selfie_path):
            os.remove(temp_selfie_path)
            
        MATCH_THRESHOLD = 0.40
        if similarity < MATCH_THRESHOLD:
            return {
                "status": "failed",
                "message": f"Face verification failed! Similarity score too low ({round(float(similarity), 2)}).",
                "similarity_score": round(float(similarity), 2)
            }

        new_attendance = models.Attendance(
            student_id=student_id,
            schedule_id=schedule_id,
            status="Present"
        )
        db.add(new_attendance)
        db.commit()
        db.refresh(new_attendance)
        
        return {
            "status": "success",
            "message": "Attendance successfully marked via Geofencing & Face Verification!",
            "distance_meters": round(distance, 2),
            "similarity_score": round(float(similarity), 2)
        }
        
    except Exception as e:
        if 'temp_selfie_path' in locals() and os.path.exists(temp_selfie_path):
            os.remove(temp_selfie_path)
        return {"status": "error", "message": str(e)}

# --- Attendance Logs Endpoint ---
@app.get("/attendance")
def get_attendance_logs(db: Session = Depends(get_db)):
    records = db.query(models.Attendance).order_by(models.Attendance.timestamp.desc()).all()
    result = []
    for r in records:
        student_name = r.student.name if r.student else f"Student #{r.student_id}"
        course_name = r.schedule.course_name if r.schedule else f"Schedule #{r.schedule_id}"
        result.append({
            "id": r.id,
            "student_id": r.student_id,
            "student_name": student_name,
            "schedule_id": r.schedule_id,
            "course_name": course_name,
            "timestamp": r.timestamp.strftime("%Y-%m-%d %H:%M:%S") if r.timestamp else None,
            "status": r.status
        })
    return result

# --- Users List Endpoint ---
@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return [{
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "role": u.role,
        "has_face_encoding": bool(u.face_encoding and os.path.exists(u.face_encoding))
    } for u in users]