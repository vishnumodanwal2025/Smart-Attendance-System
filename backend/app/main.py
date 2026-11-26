from datetime import timedelta, datetime
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

from fastapi.staticfiles import StaticFiles

# Setup directories for static face uploads and React frontend
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_DIR = os.path.join(BASE_DIR, "static", "faces")
FRONTEND_DIST = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "frontend", "dist"))
FRONTEND_DIST_ASSETS = os.path.join(FRONTEND_DIST, "assets")
FRONTEND_FILE = os.path.join(FRONTEND_DIST, "index.html") if os.path.exists(os.path.join(FRONTEND_DIST, "index.html")) else os.path.abspath(os.path.join(BASE_DIR, "..", "..", "frontend", "index.html"))
os.makedirs(UPLOAD_DIR, exist_ok=True)
if os.path.exists(FRONTEND_DIST_ASSETS):
    app.mount("/assets", StaticFiles(directory=FRONTEND_DIST_ASSETS), name="frontend-assets")

@app.on_event("startup")
def init_db_data():
    """Seed initial sample data for immediate out-of-the-box demo."""
    db = SessionLocal()
    try:
        prof_id = 2

        if db.query(models.User).count() == 0:
            user1_path = os.path.join(UPLOAD_DIR, "user_1.jpg")
            user2_path = os.path.join(UPLOAD_DIR, "user_2.jpg")
            user1 = models.User(
                name="Demo Student",
                email="student@college.edu",
                hashed_password=auth.get_password_hash("student123"),
                role="student",
                face_encoding=user1_path if os.path.exists(user1_path) else None
            )
            user2 = models.User(
                name="Demo Professor",
                email="prof@college.edu",
                hashed_password=auth.get_password_hash("prof123"),
                role="professor",
                face_encoding=user2_path if os.path.exists(user2_path) else None
            )
            db.add_all([user1, user2])
            db.commit()
            db.refresh(user1)
            db.refresh(user2)
            prof_id = user2.id
            print("[DB Seed] Seeded default users.")
        else:
            prof = db.query(models.User).filter(models.User.role == "professor").first()
            if prof:
                prof_id = prof.id

        # Seed 6 GLBAJAJ subjects if fewer than 6 schedules exist
        if db.query(models.Schedule).count() < 6:
            db.query(models.Schedule).delete()
            db.commit()
            subjects = [
                ("COA: Computer Organisation & Architecture", 27.646560, 77.551925, 1000.0),
                ("DSTL: Discrete Structures & Theory of Logic", 27.646560, 77.551925, 1000.0),
                ("MATH-4: Mathematics IV", 27.646560, 77.551925, 1000.0),
                ("DS: Data Structures", 27.646560, 77.551925, 1000.0),
                ("UHV: Universal Human Values", 27.646560, 77.551925, 1000.0),
                ("PYTHON: Python Programming", 27.646560, 77.551925, 1000.0),
            ]
            for name, lat, lng, radius in subjects:
                db.add(models.Schedule(course_name=name, lat=lat, lng=lng, allowed_radius_m=radius, prof_id=prof_id))
            db.commit()
            print("[DB Seed] Seeded 6 GLBAJAJ subject schedules.")
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
    
    if user.enrollment_no:
        existing_enroll = db.query(models.User).filter(models.User.enrollment_no == user.enrollment_no).first()
        if existing_enroll:
            raise HTTPException(
                status_code=400,
                detail=f"Enrollment number '{user.enrollment_no}' is already registered."
            )
    
    hashed_pwd = auth.get_password_hash(user.password)
    
    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pwd,
        role=user.role or "student",
        enrollment_no=user.enrollment_no,
        section=user.section or "H",
        group=user.group or "G1"
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# --- JSON Login Route (supports Email OR Student ID / Enrollment No) ---
@app.post("/auth/login")
def auth_login(data: schemas.SimpleLogin, db: Session = Depends(get_db)):
    identifier = data.email.strip()
    user = db.query(models.User).filter(
        (models.User.email == identifier) | (models.User.enrollment_no == identifier)
    ).first()
    
    if not user or not auth.verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Please verify your email / student ID and password."
        )
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": str(user.id), "role": user.role},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "enrollment_no": user.enrollment_no,
            "section": user.section,
            "group": user.group,
            "has_face_encoding": bool(user.face_encoding and os.path.exists(user.face_encoding))
        }
    }

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
        full_name=schedule.full_name,
        course_type=schedule.course_type or "theory",
        room_or_lab=schedule.room_or_lab,
        faculty_name=schedule.faculty_name,
        target_group=schedule.target_group or "All",
        time_slot=schedule.time_slot,
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


# --- Face Recognition AI Setup (YuNet + SFace) ---
YUNET_PATH = os.path.join(BASE_DIR, "yunet_face.onnx")
SFACE_PATH = os.path.join(BASE_DIR, "sface.onnx")

face_detector = None
face_recognizer = None

def get_face_ai():
    global face_detector, face_recognizer
    if face_detector is None and os.path.exists(YUNET_PATH):
        try:
            face_detector = cv2.FaceDetectorYN.create(
                model=YUNET_PATH,
                config="",
                input_size=(320, 320),
                score_threshold=0.6,
                nms_threshold=0.3,
                top_k=5000
            )
        except Exception as e:
            print("[Face AI Error] Could not load FaceDetectorYN:", e)
    if face_recognizer is None and os.path.exists(SFACE_PATH):
        try:
            face_recognizer = cv2.FaceRecognizerSF.create(
                model=SFACE_PATH,
                config=""
            )
        except Exception as e:
            print("[Face AI Error] Could not load FaceRecognizerSF:", e)
    return face_detector, face_recognizer


def process_face_verification(live_img, ref_img):
    """
    Analyzes live_img and ref_img using deep neural models.
    Returns: (is_verified: bool, score: float, message: str, face_detected: bool)
    Strictly enforces that a real face exists in live_img.
    """
    detector, recognizer = get_face_ai()
    if detector is None or recognizer is None:
        return (False, 0.0, "Face recognition AI models not available on server.", False)

    # 1. Detect face in live camera frame
    h_live, w_live = live_img.shape[:2]
    detector.setInputSize((w_live, h_live))
    _, faces_live = detector.detect(live_img)

    if faces_live is None or len(faces_live) == 0:
        return (False, 0.0, "No face detected in camera! Please look directly into the camera inside the guide box.", False)

    if len(faces_live) > 2:
        return (False, 0.0, f"Multiple faces ({len(faces_live)}) detected in camera frame! Only one person is allowed.", False)

    primary_live_face = faces_live[0]

    # 2. Detect face in reference enrolled baseline
    h_ref, w_ref = ref_img.shape[:2]
    detector.setInputSize((w_ref, h_ref))
    _, faces_ref = detector.detect(ref_img)

    if faces_ref is None or len(faces_ref) == 0:
        return (False, 0.0, "Enrolled reference image does not have a recognizable face. Please re-enroll face.", True)

    primary_ref_face = faces_ref[0]

    # 3. Align face crops using 5 facial landmarks
    aligned_live = recognizer.alignCrop(live_img, primary_live_face)
    aligned_ref = recognizer.alignCrop(ref_img, primary_ref_face)

    # 4. Extract 128D deep feature embeddings
    feat_live = recognizer.feature(aligned_live)
    feat_ref = recognizer.feature(aligned_ref)

    # 5. Compute cosine similarity match
    raw_sim = float(recognizer.match(feat_live, feat_ref, cv2.FaceRecognizerSF_FR_COSINE))

    # SFace cosine similarity threshold is 0.363
    MATCH_COSINE_THRESHOLD = 0.36
    is_match = bool(raw_sim >= MATCH_COSINE_THRESHOLD)

    # Friendly UI scale (0.0 to 1.0)
    display_score = round(max(0.0, min(1.0, (raw_sim + 0.2) / 1.2)), 2)

    if not is_match:
        return (False, display_score, f"Face verification failed! Live face does not match student baseline (Match score: {int(display_score * 100)}%).", True)

    return (True, display_score, f"Face verified successfully ({int(display_score * 100)}% biometric match)!", True)

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
            
        # Verify that the enrolled photo actually contains a human face!
        img = cv2.imread(file_path)
        if img is None:
            if os.path.exists(file_path): os.remove(file_path)
            return {"status": "error", "message": "Could not decode image file."}
        
        detector, _ = get_face_ai()
        if detector is not None:
            h, w = img.shape[:2]
            detector.setInputSize((w, h))
            _, faces = detector.detect(img)
            if faces is None or len(faces) == 0:
                if os.path.exists(file_path): os.remove(file_path)
                return {
                    "status": "error",
                    "message": "No face detected in reference photo! Please upload a clear photo with a visible face."
                }

        user.face_encoding = file_path
        db.commit()
        
        return {
            "status": "success",
            "message": f"Face baseline successfully registered for {user.name}!",
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
            return {"status": "error", "message": "Student or baseline face reference not enrolled"}
        
        reference_image_path = user.face_encoding
        if not os.path.exists(reference_image_path):
            return {"status": "error", "message": "Reference image file missing on server disk"}
        
        temp_selfie_path = os.path.join(UPLOAD_DIR, f"temp_{user_id}.jpg")
        with open(temp_selfie_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        img_ref = cv2.imread(reference_image_path)
        img_live = cv2.imread(temp_selfie_path)
        
        if os.path.exists(temp_selfie_path):
            os.remove(temp_selfie_path)

        if img_ref is None or img_live is None:
            return {"status": "error", "message": "Could not decode image files."}
            
        is_verified, score, msg, face_detected = process_face_verification(img_live, img_ref)
        
        return {
            "status": "success" if is_verified else "failed",
            "message": msg,
            "verified": is_verified,
            "face_detected": face_detected,
            "similarity_score": score
        }
        
    except Exception as e:
        if 'temp_selfie_path' in locals() and os.path.exists(temp_selfie_path):
            os.remove(temp_selfie_path)
        return {"status": "error", "message": str(e)}

# --- Unified Check-In Route (Geofencing + Deep Learning Face AI) ---
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
        if not user:
            return {"status": "error", "message": "Student record not found"}

        if not user.face_encoding or not os.path.exists(user.face_encoding):
            return {
                "status": "failed",
                "message": f"Student '{user.name}' has no face baseline registered. Ask faculty to register face in 'Face Enrollment' first.",
                "face_detected": False,
                "similarity_score": 0.0
            }

        schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
        if not schedule:
            return {"status": "error", "message": "Schedule not found"}
        
        # 1. Geofence Radar Check
        distance = calculate_distance(lat, lng, schedule.lat, schedule.lng)
        if distance > schedule.allowed_radius_m:
            return {
                "status": "failed",
                "message": f"Geofence radar failed! You are {round(distance, 1)}m away. Allowed radius is {schedule.allowed_radius_m}m.",
                "distance_meters": round(distance, 1),
                "face_detected": False
            }

        # 2. Duplicate Check-in Check (same student, same schedule, same day)
        today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        existing_att = db.query(models.Attendance).filter(
            models.Attendance.student_id == student_id,
            models.Attendance.schedule_id == schedule_id,
            models.Attendance.timestamp >= today_start
        ).first()
        if existing_att:
            return {
                "status": "already_marked",
                "message": f"Attendance is already marked Present for this class today (at {existing_att.timestamp.strftime('%H:%M:%S')}).",
                "distance_meters": round(distance, 1),
                "similarity_score": 1.0,
                "face_detected": True
            }

        # Save live camera capture
        temp_selfie_path = os.path.join(UPLOAD_DIR, f"temp_checkin_{student_id}.jpg")
        with open(temp_selfie_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        img_ref = cv2.imread(user.face_encoding)
        img_live = cv2.imread(temp_selfie_path)
        
        if os.path.exists(temp_selfie_path):
            os.remove(temp_selfie_path)

        if img_ref is None or img_live is None:
            return {"status": "error", "message": "Could not decode uploaded camera image."}

        # 3. AI Biometric Face Detection & SFace Verification
        is_verified, score, msg, face_detected = process_face_verification(img_live, img_ref)
        
        # STRICT REJECTION: If NO face is detected in the camera frame
        if not face_detected:
            return {
                "status": "failed",
                "message": msg,
                "face_detected": False,
                "similarity_score": 0.0,
                "distance_meters": round(distance, 1)
            }

        # REJECTION: If face is detected but does not match the enrolled student
        if not is_verified:
            return {
                "status": "failed",
                "message": msg,
                "face_detected": True,
                "similarity_score": score,
                "distance_meters": round(distance, 1)
            }

        # 4. Success: Mark attendance in database
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
            "message": f"Biometric Verified ({int(score * 100)}% match)! Attendance recorded Present.",
            "distance_meters": round(distance, 1),
            "similarity_score": score,
            "face_detected": True
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
        "enrollment_no": u.enrollment_no,
        "section": u.section,
        "group": u.group,
        "has_face_encoding": bool(u.face_encoding and os.path.exists(u.face_encoding))
    } for u in users]

# ============================================================
#  ATTENDANCE SESSION MANAGEMENT
#  Professor opens/closes attendance for a class.
#  Students can only check-in when a session is ACTIVE.
# ============================================================

@app.post("/sessions/open")
def open_attendance_session(schedule_id: int, prof_id: int = 1, db: Session = Depends(get_db)):
    """Professor opens attendance for a specific class."""
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    if not schedule:
        raise HTTPException(status_code=404, detail="Schedule not found")

    # Check if already open
    existing = db.query(models.AttendanceSession).filter(
        models.AttendanceSession.schedule_id == schedule_id,
        models.AttendanceSession.is_active == "yes"
    ).first()
    if existing:
        return {"status": "already_open", "message": f"Attendance for '{schedule.course_name}' is already open.", "session_id": existing.id}

    session = models.AttendanceSession(schedule_id=schedule_id, opened_by=prof_id)
    db.add(session)
    db.commit()
    db.refresh(session)
    return {
        "status": "opened",
        "message": f"Attendance OPENED for '{schedule.course_name}'",
        "session_id": session.id,
        "schedule_id": schedule_id,
        "course_name": schedule.course_name,
        "opened_at": session.opened_at.strftime("%Y-%m-%d %H:%M:%S")
    }


@app.post("/sessions/close")
def close_attendance_session(schedule_id: int, db: Session = Depends(get_db)):
    """Professor closes attendance for a specific class."""
    session = db.query(models.AttendanceSession).filter(
        models.AttendanceSession.schedule_id == schedule_id,
        models.AttendanceSession.is_active == "yes"
    ).first()
    if not session:
        raise HTTPException(status_code=404, detail="No active session found for this class")

    session.is_active = "no"
    session.closed_at = datetime.utcnow()
    db.commit()
    schedule = db.query(models.Schedule).filter(models.Schedule.id == schedule_id).first()
    return {
        "status": "closed",
        "message": f"Attendance CLOSED for '{schedule.course_name if schedule else schedule_id}'",
        "closed_at": session.closed_at.strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/sessions/active")
def get_active_sessions(db: Session = Depends(get_db)):
    """Returns all currently open attendance sessions (for students to see)."""
    sessions = db.query(models.AttendanceSession).filter(
        models.AttendanceSession.is_active == "yes"
    ).all()
    result = []
    for s in sessions:
        schedule = s.schedule
        prof = s.professor
        result.append({
            "session_id": s.id,
            "schedule_id": s.schedule_id,
            "course_name": schedule.course_name if schedule else f"Schedule #{s.schedule_id}",
            "full_name": schedule.full_name if schedule else "",
            "course_type": schedule.course_type if schedule else "theory",
            "room_or_lab": schedule.room_or_lab if schedule else "",
            "faculty_name": schedule.faculty_name if schedule else "",
            "target_group": schedule.target_group if schedule else "All",
            "time_slot": schedule.time_slot if schedule else "",
            "opened_by_name": prof.name if prof else f"Professor #{s.opened_by}",
            "opened_at": s.opened_at.strftime("%Y-%m-%d %H:%M:%S"),
            "lat": schedule.lat if schedule else None,
            "lng": schedule.lng if schedule else None,
            "allowed_radius_m": schedule.allowed_radius_m if schedule else 200
        })
    return result


@app.get("/sessions/history")
def get_session_history(db: Session = Depends(get_db)):
    """Returns all past sessions (closed)."""
    sessions = db.query(models.AttendanceSession).order_by(
        models.AttendanceSession.opened_at.desc()
    ).all()
    result = []
    for s in sessions:
        schedule = s.schedule
        prof = s.professor
        result.append({
            "session_id": s.id,
            "schedule_id": s.schedule_id,
            "course_name": schedule.course_name if schedule else f"Schedule #{s.schedule_id}",
            "opened_by_name": prof.name if prof else f"Professor #{s.opened_by}",
            "opened_at": s.opened_at.strftime("%Y-%m-%d %H:%M:%S"),
            "closed_at": s.closed_at.strftime("%Y-%m-%d %H:%M:%S") if s.closed_at else None,
            "is_active": s.is_active
        })
    return result
