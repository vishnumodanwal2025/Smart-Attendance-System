import os

target_files = [
    r"c:\Users\vishn\OneDrive\Desktop\New folder\attendance-system\frontend\index.html",
    r"c:\Users\vishn\OneDrive\Desktop\New folder\attendance-system\build_full_frontend.py"
]

old_chunk_1 = """      if (data.status === 'success') {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'success', 'Attendance Verified Successfully!', data.message);
        if (data.similarity_score !== undefined) {
          const pct = Math.min(100, Math.round(data.similarity_score * 100));
          simWrap.className = 'similarity-bar-wrap show';
          simText.textContent = pct + '%';
          simFill.style.width = pct + '%';
        }
        showGlobalToast('success', 'Attendance Marked: Present');
        loadAttendanceLogs();
      } else {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'Check-In Denied', data.message || 'Verification could not be confirmed.');
      }"""

new_chunk_1 = """      if (data.status === 'success') {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'success', 'Attendance Verified Successfully!', data.message);
        if (data.similarity_score !== undefined) {
          const pct = Math.min(100, Math.round(data.similarity_score * 100));
          simWrap.className = 'similarity-bar-wrap show';
          simText.textContent = pct + '%';
          simFill.style.width = pct + '%';
        }
        showGlobalToast('success', 'Attendance Marked: Present');
        loadAttendanceLogs();
      } else if (data.status === 'already_marked') {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'warning', 'Already Recorded Today', data.message);
        showGlobalToast('info', 'Attendance already marked for this class today.');
      } else if (data.face_detected === false) {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'No Face Detected in Camera', data.message || 'Please look straight into the camera in good lighting.');
        showGlobalToast('error', 'No face detected! Look directly into the camera.');
      } else {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'Check-In Denied', data.message || 'Verification could not be confirmed.');
        showGlobalToast('error', data.message || 'Verification failed.');
      }"""

old_chunk_2 = """      if (data.status === 'success') {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'success', 'Verified', data.message);
        loadAttendanceLogs();
      } else {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'Failed', data.message);
      }"""

new_chunk_2 = """      if (data.status === 'success') {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'success', 'Verified', data.message);
        loadAttendanceLogs();
      } else if (data.status === 'already_marked') {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'warning', 'Already Marked Today', data.message);
      } else if (data.face_detected === false) {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'No Face Detected in Camera', data.message || 'No face detected in frame.');
      } else {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'Failed', data.message);
      }"""

for fpath in target_files:
    if not os.path.exists(fpath): continue
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Normalize
    content_norm = content.replace("\r\n", "\n")
    old_1_norm = old_chunk_1.replace("\r\n", "\n")
    old_2_norm = old_chunk_2.replace("\r\n", "\n")

    if old_1_norm in content_norm:
        content_norm = content_norm.replace(old_1_norm, new_chunk_1)
        print(f"Updated checkin response handler in {os.path.basename(fpath)}")
    else:
        print(f"Could not find old_chunk_1 in {os.path.basename(fpath)}")

    if old_2_norm in content_norm:
        content_norm = content_norm.replace(old_2_norm, new_chunk_2)
        print(f"Updated prof checkin handler in {os.path.basename(fpath)}")
    else:
        print(f"Could not find old_chunk_2 in {os.path.basename(fpath)}")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(content_norm)

print("Frontend checkin handlers updated successfully!")
