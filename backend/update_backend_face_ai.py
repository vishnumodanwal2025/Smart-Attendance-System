import re

main_path = "app/main.py"
with open(main_path, "r", encoding="utf-8") as f:
    code = f.read()

# Normalize newlines
code = code.replace("\r\n", "\n")

# Model paths and helper function definition
face_ai_helpers = '''
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
'''

# Insert helper before upload-face route
if "get_face_ai" not in code:
    upload_marker = '# --- Upload Face Reference Route ---'
    if upload_marker in code:
        code = code.replace(upload_marker, face_ai_helpers + "\n" + upload_marker)
        print("Inserted face_ai_helpers")
    else:
        print("Could not find upload_marker!")

# Replace upload_face implementation to validate face presence on enrollment
old_upload_face = re.search(r'# --- Upload Face Reference Route ---.*?(?=# --- OpenCV Face Verification Route ---)', code, re.DOTALL)
new_upload_face = '''# --- Upload Face Reference Route ---
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

'''

if old_upload_face:
    code = code[:old_upload_face.start()] + new_upload_face + code[old_upload_face.end():]
    print("Replaced upload_face endpoint")
else:
    print("Could not match old_upload_face")

# Replace verify_student_face and unified_check_in
old_checkin_block = re.search(r'# --- OpenCV Face Verification Route ---.*?(?=# --- Attendance Logs Endpoint ---)', code, re.DOTALL)
new_checkin_block = '''# --- OpenCV Face Verification Route ---
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

'''

if old_checkin_block:
    code = code[:old_checkin_block.start()] + new_checkin_block + code[old_checkin_block.end():]
    print("Replaced checkin endpoints")
else:
    print("Could not match old_checkin_block")

with open(main_path, "w", encoding="utf-8") as f:
    f.write(code)

print("Updated app/main.py successfully!")
