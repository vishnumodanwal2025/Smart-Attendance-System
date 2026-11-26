import re

main_path = "app/main.py"
with open(main_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update register_user and add /auth/login
old_register_and_login = '''# --- User Registration Route ---
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

# --- User Login Route ---'''

new_register_and_login = '''# --- User Registration Route ---
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

# --- User Login Route ---'''

# Normalize newlines for matching
content_norm = content.replace("\r\n", "\n")
old_register_norm = old_register_and_login.replace("\r\n", "\n")

if old_register_norm in content_norm:
    content_norm = content_norm.replace(old_register_norm, new_register_and_login)
    print("Successfully replaced register and added /auth/login")
else:
    print("Could not find old register pattern!")

# 2. Update create_schedule
old_create_sched = '''def create_schedule(schedule: schemas.ScheduleCreate, current_user_id: int = 1, db: Session = Depends(get_db)):
    new_schedule = models.Schedule(
        course_name=schedule.course_name,
        lat=schedule.lat,
        lng=schedule.lng,
        allowed_radius_m=schedule.allowed_radius_m,
        prof_id=current_user_id
    )'''

new_create_sched = '''def create_schedule(schedule: schemas.ScheduleCreate, current_user_id: int = 1, db: Session = Depends(get_db)):
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
    )'''

old_create_sched_norm = old_create_sched.replace("\r\n", "\n")
if old_create_sched_norm in content_norm:
    content_norm = content_norm.replace(old_create_sched_norm, new_create_sched)
    print("Successfully updated create_schedule")
else:
    print("Could not find old create_schedule pattern!")

# 3. Update get_users
old_get_users = '''@app.get("/users")
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return [{
        "id": u.id,
        "name": u.name,
        "email": u.email,
        "role": u.role,
        "has_face_encoding": bool(u.face_encoding and os.path.exists(u.face_encoding))
    } for u in users]'''

new_get_users = '''@app.get("/users")
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
    } for u in users]'''

old_get_users_norm = old_get_users.replace("\r\n", "\n")
if old_get_users_norm in content_norm:
    content_norm = content_norm.replace(old_get_users_norm, new_get_users)
    print("Successfully updated get_users")
else:
    print("Could not find old get_users pattern!")

# 4. Update get_active_sessions to include schedule details
old_active_sess = '''        result.append({
            "session_id": s.id,
            "schedule_id": s.schedule_id,
            "course_name": schedule.course_name if schedule else f"Schedule #{s.schedule_id}",
            "opened_by_name": prof.name if prof else f"Professor #{s.opened_by}",
            "opened_at": s.opened_at.strftime("%Y-%m-%d %H:%M:%S"),
            "lat": schedule.lat if schedule else None,
            "lng": schedule.lng if schedule else None,
            "allowed_radius_m": schedule.allowed_radius_m if schedule else 200
        })'''

new_active_sess = '''        result.append({
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
        })'''

old_active_sess_norm = old_active_sess.replace("\r\n", "\n")
if old_active_sess_norm in content_norm:
    content_norm = content_norm.replace(old_active_sess_norm, new_active_sess)
    print("Successfully updated get_active_sessions")
else:
    print("Could not find old active sessions pattern!")

with open(main_path, "w", encoding="utf-8") as f:
    f.write(content_norm)

print("Saved updated app/main.py")
