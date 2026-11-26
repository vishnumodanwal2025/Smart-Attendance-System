# Smart Attendance AI System

A full-stack college attendance application for managing class sessions and
recording attendance with live face verification and campus geofencing.

## Features

- Student and faculty registration and sign-in
- Faculty-controlled open and close attendance sessions
- Student face enrollment by image upload or camera capture
- Face detection and matching with OpenCV YuNet and SFace ONNX models
- Location checks using the schedule's configured geofence
- Duplicate attendance prevention for the same student, course, and day
- Theory and lab timetable views
- Searchable attendance logs and session history

## Technology

- Frontend: React, Vite, JavaScript, CSS, lucide-react
- Backend: Python, FastAPI, SQLAlchemy, Pydantic
- Computer vision: OpenCV, YuNet, SFace, ONNX
- Database: SQLite by default; SQLAlchemy-compatible remote databases can be
  configured with `DATABASE_URL`

## Run locally

Requirements: Python 3, Node.js, npm, and the face model files in
`backend/app/`.

From the project root, install backend dependencies and start the API:

```powershell
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --reload --port 8000
```

In another terminal, start the frontend:

```powershell
cd frontend
npm install
npm run dev
```

The frontend is configured to call `http://127.0.0.1:8000`. Open the URL
printed by Vite (usually `http://localhost:5173`). Camera and location access
are required for live student check-in.

## Data and privacy

The application stores attendance in a local SQLite database. Student face
reference uploads are stored under `backend/app/static/faces/`; these biometric
images are intentionally excluded from version control. Enroll a reference
face through the faculty interface when running the application locally.
Database files, virtual environments, and local environment files should not
be committed.

This project is an academic/demo application. Review authentication,
authorization, privacy, CORS, and deployment settings before any production
use. In particular, configure a secure JWT secret rather than using the
development key in `backend/app/auth.py`.

For a fuller feature, data model, and API overview, see
[`PROJECT_DETAILS.txt`](PROJECT_DETAILS.txt).
