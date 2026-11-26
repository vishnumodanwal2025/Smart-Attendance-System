import React, { useState, useEffect, useCallback } from 'react';
import './index.css';

import { API_BASE, STATIC_SCHEDULE_DATA } from './constants/scheduleData';
import AuthOverlay from './components/AuthOverlay';
import Topbar from './components/Topbar';
import TabNav from './components/TabNav';
import LiveCheckinPanel from './components/LiveCheckinPanel';
import ManageSessionsPanel from './components/ManageSessionsPanel';
import FaceEnrollmentPanel from './components/FaceEnrollmentPanel';
import TimetablePanel from './components/TimetablePanel';
import AttendanceLogsPanel from './components/AttendanceLogsPanel';
import Toast from './components/Toast';

export default function App() {
  const [currentUser, setCurrentUser] = useState(() => {
    try {
      const saved = localStorage.getItem('glbajaj_user');
      if (saved) {
        const user = JSON.parse(saved);
        // Restore body class on page reload
        document.body.classList.remove('role-student', 'role-professor');
        document.body.classList.add('role-' + user.role);
        return user;
      }
      return null;
    } catch {
      return null;
    }
  });

  const [activeTab, setActiveTab] = useState('checkin');
  const [backendOnline, setBackendOnline] = useState(false);
  const [cameraActive, setCameraActive] = useState(false);

  const [availableSchedules, setAvailableSchedules] = useState(STATIC_SCHEDULE_DATA);
  const [enrolledStudents, setEnrolledStudents] = useState([]);
  const [activeSessions, setActiveSessions] = useState([]);
  const [attendanceLogs, setAttendanceLogs] = useState([]);
  const [loadingLogs, setLoadingLogs] = useState(false);

  const [toast, setToast] = useState({ show: false, type: 'info', message: '' });

  const showToast = useCallback((type, message) => {
    setToast({ show: true, type, message });
    setTimeout(() => {
      setToast((prev) => ({ ...prev, show: false }));
    }, 3800);
  }, []);

  // Check backend health
  const checkHealth = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/api/health`, {
        signal: AbortSignal.timeout(4000)
      });
      if (res.ok) setBackendOnline(true);
      else setBackendOnline(false);
    } catch {
      setBackendOnline(false);
    }
  }, []);

  useEffect(() => {
    checkHealth();
    const timer = setInterval(checkHealth, 15000);
    return () => clearInterval(timer);
  }, [checkHealth]);

  // Load schedules
  const loadSchedules = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/schedules`);
      if (res.ok) {
        const backendData = await res.json();
        const merged = STATIC_SCHEDULE_DATA.map((st) => {
          const match = backendData.find((b) => b.id === st.id);
          return match ? { ...st, ...match } : st;
        });
        setAvailableSchedules(merged);
      }
    } catch {
      setAvailableSchedules(STATIC_SCHEDULE_DATA);
    }
  }, []);

  // Load users
  const loadUsers = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/users`);
      if (res.ok) {
        const users = await res.json();
        const students = users.filter((u) => u.role === 'student');
        setEnrolledStudents(students);
      }
    } catch {
      setEnrolledStudents([
        { id: 1, name: 'Student Demo (25CSAIM076)', enrollment_no: '25CSAIM076', role: 'student', has_face_encoding: true }
      ]);
    }
  }, []);

  // Load active sessions
  const loadActiveSessions = useCallback(async () => {
    try {
      const res = await fetch(`${API_BASE}/sessions/active`);
      if (res.ok) {
        const data = await res.json();
        setActiveSessions(Array.isArray(data) ? data : []);
      }
    } catch {
      setActiveSessions([]);
    }
  }, []);

  // Load attendance logs
  const loadAttendanceLogs = useCallback(async () => {
    setLoadingLogs(true);
    try {
      const res = await fetch(`${API_BASE}/attendance`);
      if (res.ok) {
        const logs = await res.json();
        setAttendanceLogs(Array.isArray(logs) ? logs : []);
      }
    } catch {
      setAttendanceLogs([]);
    } finally {
      setLoadingLogs(false);
    }
  }, []);

  // Initialize and poll data once user is logged in
  useEffect(() => {
    if (currentUser) {
      loadSchedules();
      loadUsers();
      loadActiveSessions();
      loadAttendanceLogs();

      // Poll active sessions periodically for students
      let sessionPollTimer = null;
      if (currentUser.role === 'student') {
        sessionPollTimer = setInterval(loadActiveSessions, 10000);
      }

      return () => {
        if (sessionPollTimer) clearInterval(sessionPollTimer);
      };
    }
  }, [currentUser, loadSchedules, loadUsers, loadActiveSessions, loadAttendanceLogs]);

  const handleLoginSuccess = (user) => {
    setCurrentUser(user);
    // Set body role class so CSS faculty-only display rules work (matches original HTML)
    document.body.classList.remove('role-student', 'role-professor');
    document.body.classList.add('role-' + user.role);
    try {
      localStorage.setItem('glbajaj_user', JSON.stringify(user));
    } catch {}
    setActiveTab('checkin');
  };

  const handleLogout = () => {
    setCurrentUser(null);
    document.body.classList.remove('role-student', 'role-professor');
    try {
      localStorage.removeItem('glbajaj_user');
    } catch {}
    showToast('info', 'Logged out.');
  };

  return (
    <>
      {!currentUser ? (
        <AuthOverlay
          onLoginSuccess={handleLoginSuccess}
          showToast={showToast}
        />
      ) : (
        <div id="appShell" className="visible">
          <Topbar
            backendOnline={backendOnline}
            cameraActive={cameraActive}
            currentUser={currentUser}
            onLogout={handleLogout}
          />

          <TabNav
            activeTab={activeTab}
            setActiveTab={(tab) => {
              // Guard: students cannot access faculty-only tabs
              if ((tab === 'sessions' || tab === 'enroll') && currentUser.role !== 'professor') return;
              setActiveTab(tab);
            }}
          />

          <main className="app-main-content">
            {activeTab === 'checkin' && (
              <LiveCheckinPanel
                currentUser={currentUser}
                activeSessions={activeSessions}
                availableSchedules={availableSchedules}
                enrolledStudents={enrolledStudents}
                onRefreshSessions={loadActiveSessions}
                onAttendanceMarked={loadAttendanceLogs}
                showToast={showToast}
                setCameraActive={setCameraActive}
              />
            )}

            {activeTab === 'sessions' && currentUser.role === 'professor' && (
              <ManageSessionsPanel
                currentUser={currentUser}
                availableSchedules={availableSchedules}
                showToast={showToast}
                onSessionUpdated={loadActiveSessions}
              />
            )}

            {activeTab === 'enroll' && currentUser.role === 'professor' && (
              <FaceEnrollmentPanel
                enrolledStudents={enrolledStudents}
                onStudentEnrolled={loadUsers}
                showToast={showToast}
              />
            )}

            {activeTab === 'schedules' && (
              <TimetablePanel availableSchedules={availableSchedules} />
            )}

            {activeTab === 'history' && (
              <AttendanceLogsPanel
                attendanceLogs={attendanceLogs}
                loadingLogs={loadingLogs}
                onRefreshLogs={loadAttendanceLogs}
              />
            )}
          </main>
        </div>
      )}

      <Toast toast={toast} />
    </>
  );
}
