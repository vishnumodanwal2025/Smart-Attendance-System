import urllib.request
import urllib.parse
import json
import cv2
import numpy as np

# Create blank image (no face)
blank = np.zeros((480, 640, 3), dtype=np.uint8)
cv2.imwrite("test_noface.jpg", blank)

boundary = "----WebKitFormBoundary7MA4YWxkTrZu0gW"
header_part = (
    f"--{boundary}\r\n"
    f"Content-Disposition: form-data; name=\"file\"; filename=\"test_noface.jpg\"\r\n"
    f"Content-Type: image/jpeg\r\n\r\n"
).encode("utf-8")
footer_part = f"\r\n--{boundary}--\r\n".encode("utf-8")

with open("test_noface.jpg", "rb") as f:
    file_bytes = f.read()

payload = header_part + file_bytes + footer_part

url = "http://127.0.0.1:8000/attendance/unified-check-in?student_id=1&schedule_id=2&lat=27.646560&lng=77.551925"
req = urllib.request.Request(url, data=payload, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})

try:
    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode())
        print("Check-in response with NO FACE:")
        print(json.dumps(result, indent=2))
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code, e.read().decode())
