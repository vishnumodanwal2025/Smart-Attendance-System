import React, { useState, useEffect, useRef, useCallback } from 'react';
import { RefreshCw, Camera, AlertCircle } from 'lucide-react';
import { API_BASE, CAMPUS_COORDINATES, calculateHaversine } from '../constants/scheduleData';

export default function LiveCheckinPanel({
  currentUser,
  activeSessions,
  availableSchedules,
  enrolledStudents,
  onRefreshSessions,
  onAttendanceMarked,
  showToast,
  setCameraActive,
}) {
  const isFaculty = currentUser?.role === 'professor';

  /* ─── GPS / Geofence ─────────────────────────────────────── */
  const [useDemoGps, setUseDemoGps]       = useState(true);
  const [currentPosition, setCurrentPos] = useState(CAMPUS_COORDINATES);

  /* ─── Student checkin state ──────────────────────────────── */
  const [selectedStudentId,  setSelectedStudentId]  = useState(currentUser?.id || '');
  const [selectedScheduleId, setSelectedScheduleId] = useState('');
  const [studentVerifying,   setStudentVerifying]   = useState(false);
  const [checkinResult,      setCheckinResult]       = useState(null);

  /* ─── Faculty checkin state ──────────────────────────────── */
  const [profStudentId,  setProfStudentId]  = useState('');
  const [profScheduleId, setProfScheduleId] = useState('');
  const [profVerifying,  setProfVerifying]  = useState(false);
  const [profResult,     setProfResult]     = useState(null);

  /* ─── Webcam refs (one shared stream, two video elements) ── */
  const studentVideoRef = useRef(null);
  const profVideoRef    = useRef(null);
  const canvasRef       = useRef(null);
  const streamRef       = useRef(null);
  const [cameraBlocked, setCameraBlocked] = useState(false);

  /* ─── Sync default selections ────────────────────────────── */
  useEffect(() => {
    if (currentUser?.role === 'student' && currentUser?.id) {
      setSelectedStudentId(currentUser.id);
    } else if (enrolledStudents.length > 0 && !selectedStudentId) {
      setSelectedStudentId(enrolledStudents[0].id);
    }
    if (enrolledStudents.length > 0 && !profStudentId) {
      setProfStudentId(enrolledStudents[0].id);
    }
  }, [currentUser, enrolledStudents]);

  useEffect(() => {
    if (activeSessions.length > 0) {
      if (!selectedScheduleId || !activeSessions.some(s => s.schedule_id === Number(selectedScheduleId))) {
        setSelectedScheduleId(activeSessions[0].schedule_id);
      }
    }
  }, [activeSessions]);

  useEffect(() => {
    if (availableSchedules.length > 0 && !profScheduleId) {
      setProfScheduleId(availableSchedules[0].id);
    }
  }, [availableSchedules]);

  /* ─── GPS ───────────────────────────────────────────────── */
  useEffect(() => {
    if (useDemoGps) {
      setCurrentPos(CAMPUS_COORDINATES);
    } else if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        pos => setCurrentPos({ lat: pos.coords.latitude, lng: pos.coords.longitude }),
        ()  => { setUseDemoGps(true); setCurrentPos(CAMPUS_COORDINATES); }
      );
    }
  }, [useDemoGps]);

  /* ─── Webcam ─────────────────────────────────────────────── */
  const startCamera = useCallback(async () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(t => t.stop());
    }
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' },
      });
      streamRef.current = stream;
      if (studentVideoRef.current) studentVideoRef.current.srcObject = stream;
      if (profVideoRef.current)    profVideoRef.current.srcObject    = stream;
      setCameraBlocked(false);
      setCameraActive(true);
    } catch (err) {
      console.warn('Camera error:', err);
      setCameraBlocked(true);
      setCameraActive(false);
    }
  }, [setCameraActive]);

  useEffect(() => {
    startCamera();
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(t => t.stop());
        streamRef.current = null;
      }
      setCameraActive(false);
    };
  }, [startCamera]);

  /* ─── Distance ───────────────────────────────────────────── */
  const currentSched =
    availableSchedules.find(s => s.id === Number(selectedScheduleId)) ||
    activeSessions.find(s => s.schedule_id === Number(selectedScheduleId));

  const distance = currentSched
    ? calculateHaversine(
        currentPosition.lat, currentPosition.lng,
        currentSched.lat || CAMPUS_COORDINATES.lat,
        currentSched.lng || CAMPUS_COORDINATES.lng,
      )
    : 0;

  const allowedRadius  = currentSched?.allowed_radius_m || 100;
  const isInsideRadar  = distance <= allowedRadius;

  /* ─── Frame capture helper ───────────────────────────────── */
  const captureFrameBlob = (videoEl) => {
    return new Promise(resolve => {
      const canvas = canvasRef.current || document.createElement('canvas');
      canvas.width  = videoEl?.videoWidth  || 640;
      canvas.height = videoEl?.videoHeight || 480;
      const ctx = canvas.getContext('2d');
      if (videoEl && ctx) {
        ctx.save();
        ctx.scale(-1, 1);
        ctx.drawImage(videoEl, -canvas.width, 0, canvas.width, canvas.height);
        ctx.restore();
      }
      canvas.toBlob(blob => resolve(blob), 'image/jpeg', 0.92);
    });
  };

  /* ─── Student Check-In ───────────────────────────────────── */
  const handleStudentCheckin = async () => {
    if (!selectedScheduleId) {
      setCheckinResult({ status: 'warning', title: 'No Class Selected', message: 'Please select an active session.', similarity: null });
      return;
    }
    setStudentVerifying(true);
    setCheckinResult(null);
    try {
      const blob = await captureFrameBlob(studentVideoRef.current);
      const formData = new FormData();
      formData.append('file', blob, 'checkin_selfie.jpg');

      const stuId = selectedStudentId || currentUser?.id || 1;
      const url   = `${API_BASE}/attendance/unified-check-in?student_id=${stuId}&schedule_id=${selectedScheduleId}&lat=${currentPosition.lat}&lng=${currentPosition.lng}`;
      const res   = await fetch(url, { method: 'POST', body: formData });
      const data  = await res.json();
      setStudentVerifying(false);

      if (data.status === 'success') {
        const pct = data.similarity_score !== undefined ? Math.min(100, Math.round(data.similarity_score * 100)) : null;
        setCheckinResult({ status: 'success', title: 'Attendance Verified Successfully!', message: data.message || 'Marked Present.', similarity: pct });
        showToast('success', 'Attendance Marked: Present');
        onAttendanceMarked?.();
      } else if (data.status === 'already_marked') {
        setCheckinResult({ status: 'warning', title: 'Already Recorded Today', message: data.message, similarity: null });
        showToast('info', 'Already marked for this class today.');
      } else if (data.face_detected === false) {
        setCheckinResult({ status: 'error', title: 'No Face Detected', message: data.message || 'Look straight into the camera in good lighting.', similarity: null });
        showToast('error', 'No face detected! Look directly into the camera.');
      } else {
        setCheckinResult({ status: 'error', title: 'Check-In Denied', message: data.message || 'Verification failed.', similarity: null });
        showToast('error', data.message || 'Verification failed.');
      }
    } catch (err) {
      setStudentVerifying(false);
      setCheckinResult({ status: 'error', title: 'Network Error', message: err.message, similarity: null });
    }
  };

  /* ─── Faculty Direct Check-In ────────────────────────────── */
  const handleProfCheckin = async () => {
    if (!profStudentId || !profScheduleId) {
      setProfResult({ status: 'warning', title: 'Missing Selection', message: 'Select both student and schedule.' });
      return;
    }
    setProfVerifying(true);
    setProfResult(null);
    try {
      const blob = await captureFrameBlob(profVideoRef.current || studentVideoRef.current);
      const formData = new FormData();
      formData.append('file', blob, 'faculty_checkin.jpg');

      const url  = `${API_BASE}/attendance/unified-check-in?student_id=${profStudentId}&schedule_id=${profScheduleId}&lat=${CAMPUS_COORDINATES.lat}&lng=${CAMPUS_COORDINATES.lng}`;
      const res  = await fetch(url, { method: 'POST', body: formData });
      const data = await res.json();
      setProfVerifying(false);

      if (data.status === 'success') {
        setProfResult({ status: 'success', title: 'Verified', message: data.message });
        showToast('success', 'Attendance recorded.');
        onAttendanceMarked?.();
      } else if (data.status === 'already_marked') {
        setProfResult({ status: 'warning', title: 'Already Marked Today', message: data.message });
      } else if (data.face_detected === false) {
        setProfResult({ status: 'error', title: 'No Face Detected', message: data.message || 'No face in frame.' });
      } else {
        setProfResult({ status: 'error', title: 'Verification Failed', message: data.message });
      }
    } catch (err) {
      setProfVerifying(false);
      setProfResult({ status: 'error', title: 'Error', message: err.message });
    }
  };

  const firstSession = activeSessions[0] || null;

  /* ─── Render ─────────────────────────────────────────────── */
  return (
    <div className="tab-panel active">

      {/* Hero */}
      <div className="page-hero-banner">
        <div>
          <div className="page-hero-title">Live Attendance Verification</div>
          <div className="page-hero-sub">AI Biometric Face Verification + Campus Geofence Radar System</div>
          <div className="page-hero-tags">
            <span className="hero-tag">Room 242 (Block-B)</span>
            <span className="hero-tag">Section H &bull; Year 2 &bull; Sem III</span>
            <span className="hero-tag">CSE-AIML &amp; CS</span>
          </div>
        </div>
      </div>

      {/* ── STUDENT VIEW ──────────────────────────────────────── */}
      {!isFaculty && (
        <>
          {/* Waiting gate when no session is open */}
          {activeSessions.length === 0 ? (
            <div className="session-empty-gate">
              <div className="gate-icon-circle">
                <AlertCircle size={34} />
              </div>
              <div className="gate-title">Attendance Session Not Active</div>
              <div className="gate-desc">
                Your professor has not opened attendance yet. It will appear here automatically when opened.
              </div>
              <button
                className="auth-btn primary"
                style={{ width: 'auto', padding: '10px 24px' }}
                onClick={onRefreshSessions}
              >
                <RefreshCw size={14} style={{ display: 'inline', marginRight: 6 }} />
                Refresh Status Now
              </button>
            </div>
          ) : (
            <>
              {/* Active session spotlight */}
              {firstSession && (
                <div className="active-session-spotlight">
                  <div className="session-spotlight-left">
                    <div className="live-pulse-dot" />
                    <div>
                      <div className="spotlight-class-name">
                        {firstSession.course_name}
                        {firstSession.full_name ? ` (${firstSession.full_name})` : ''}
                      </div>
                      <div className="spotlight-class-meta">
                        Opened by {firstSession.opened_by_name || 'Professor'} at {firstSession.opened_at || ''}
                        {firstSession.room_or_lab   ? ` • ${firstSession.room_or_lab}`   : ''}
                        {firstSession.target_group  ? ` • ${firstSession.target_group}`  : ''}
                      </div>
                    </div>
                  </div>
                  <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                    <span className="badge badge-success">Session Open</span>
                    <span className={`badge ${firstSession.course_type === 'lab' ? 'badge-lab' : 'badge-theory'}`}>
                      {firstSession.course_type === 'lab' ? 'Lab Session' : 'Theory Class'}
                    </span>
                  </div>
                </div>
              )}

              {/* Check-in layout */}
              <div className="checkin-layout-grid">

                {/* Left: Identity & Geofence */}
                <div className="dashboard-card card-blue">
                  <div className="card-head">
                    <div>
                      <div className="card-heading">1. Identity &amp; Geofence Verification</div>
                      <div className="card-subheading">Verify student match and location accuracy</div>
                    </div>
                  </div>

                  <div className="field-group">
                    <label className="field-label">Student Name / Profile</label>
                    <select
                      className="field-select"
                      value={selectedStudentId}
                      onChange={e => setSelectedStudentId(e.target.value)}
                    >
                      {enrolledStudents.map(stu => (
                        <option key={stu.id} value={stu.id}>
                          {stu.name}{stu.enrollment_no ? ` (${stu.enrollment_no})` : ''}
                          {stu.group ? ` [${stu.group}]` : ''}
                          {stu.has_face_encoding ? ' [Face ✓]' : ' [No Face]'}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="field-group">
                    <label className="field-label">Active Class / Lab Session</label>
                    <select
                      className="field-select"
                      value={selectedScheduleId}
                      onChange={e => setSelectedScheduleId(e.target.value)}
                    >
                      {activeSessions.map(sess => (
                        <option key={sess.session_id} value={sess.schedule_id}>
                          {sess.course_name} {sess.course_type === 'lab' ? '[LAB]' : '[Theory]'}
                        </option>
                      ))}
                    </select>
                  </div>

                  {/* Geofence radar */}
                  <div className="radar-box">
                    <div className="radar-header-row">
                      <span style={{ fontSize: 13, fontWeight: 800, color: 'var(--text)' }}>Geofence Radar</span>
                      <span className={`badge ${isInsideRadar ? 'badge-success' : 'badge-error'}`}>
                        {isInsideRadar ? 'Inside Campus Radar' : `${distance.toFixed(0)}m Away (Outside)`}
                      </span>
                    </div>
                    <label style={{ display: 'flex', alignItems: 'center', gap: 8, fontSize: 12, color: 'var(--text-muted)', cursor: 'pointer' }}>
                      <input type="checkbox" checked={useDemoGps} onChange={e => setUseDemoGps(e.target.checked)} />
                      <span>Use GL Bajaj Mathura Campus Coordinates (27.6465° N, 77.5519° E)</span>
                    </label>
                    <div className="coord-chips-row">
                      <span className="coord-chip">Lat: <strong>{currentPosition.lat.toFixed(6)}</strong></span>
                      <span className="coord-chip">Lng: <strong>{currentPosition.lng.toFixed(6)}</strong></span>
                    </div>
                    <div className="distance-stat-card">
                      <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>Radar Distance:</span>
                      <span className="distance-value-text">{distance.toFixed(1)} m (Radius: {allowedRadius} m)</span>
                    </div>
                  </div>

                  {/* Check-in result */}
                  {checkinResult && (
                    <div className={`verify-result-box show ${checkinResult.status}`}>
                      <div className="verify-result-title">{checkinResult.title}</div>
                      <div>{checkinResult.message}</div>
                      {checkinResult.similarity !== null && (
                        <div className="similarity-bar-wrap show">
                          <div className="sim-labels-row">
                            <span>OpenCV Face Correlation Match:</span>
                            <strong>{checkinResult.similarity}%</strong>
                          </div>
                          <div className="sim-track">
                            <div className="sim-fill" style={{ width: `${checkinResult.similarity}%` }} />
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>

                {/* Right: Biometric Camera */}
                <div className="dashboard-card card-teal">
                  <div className="card-head">
                    <div>
                      <div className="card-heading">2. Biometric Facial Verification</div>
                      <div className="card-subheading">Look into camera and align face inside the frame</div>
                    </div>
                    <button className="tt-filter-btn" style={{ padding: '6px 14px', fontSize: 11 }} onClick={startCamera}>
                      <Camera size={12} style={{ display: 'inline', marginRight: 4 }} />
                      Restart Cam
                    </button>
                  </div>

                  <div className="camera-viewport">
                    <video ref={studentVideoRef} autoPlay playsInline muted />
                    <div className="camera-reticle-overlay">
                      <div className="face-target-reticle">
                        <div className="radar-scan-line" />
                      </div>
                    </div>
                    {cameraBlocked && (
                      <div className="camera-blocked-fallback" style={{ display: 'flex' }}>
                        <AlertCircle size={40} />
                        <div>Camera access required.<br />Allow browser camera permissions.</div>
                      </div>
                    )}
                  </div>

                  <button
                    className="auth-btn primary"
                    style={{ padding: 14, fontSize: 14 }}
                    onClick={handleStudentCheckin}
                    disabled={studentVerifying}
                  >
                    {studentVerifying && <span className="btn-loader" />}
                    <span>
                      {studentVerifying ? 'Verifying Face & Radar...' : 'Capture Face & Verify Attendance'}
                    </span>
                  </button>
                </div>
              </div>
            </>
          )}
        </>
      )}

      {/* ── FACULTY DIRECT CHECK-IN VIEW ──────────────────────── */}
      {isFaculty && (
        <div className="dashboard-card card-red" style={{ marginBottom: 24 }}>
          <div className="card-head">
            <div>
              <div className="card-heading">Faculty Direct Attendance Verification</div>
              <div className="card-subheading">Select any enrolled student and schedule to verify check-in directly</div>
            </div>
            <button className="tt-filter-btn" style={{ padding: '6px 14px', fontSize: 11 }} onClick={startCamera}>
              <Camera size={12} style={{ display: 'inline', marginRight: 4 }} />
              Restart Cam
            </button>
          </div>

          <div className="checkin-layout-grid">
            {/* Left: Controls */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <div className="field-group">
                <label className="field-label">Select Student</label>
                <select className="field-select" value={profStudentId} onChange={e => setProfStudentId(e.target.value)}>
                  {enrolledStudents.map(stu => (
                    <option key={stu.id} value={stu.id}>
                      {stu.name}{stu.enrollment_no ? ` (${stu.enrollment_no})` : ''}
                      {stu.group ? ` - ${stu.group}` : ''}
                      {stu.has_face_encoding ? ' [Face ✓]' : ' [No Face]'}
                    </option>
                  ))}
                </select>
              </div>

              <div className="field-group">
                <label className="field-label">Select Class / Lab</label>
                <select className="field-select" value={profScheduleId} onChange={e => setProfScheduleId(e.target.value)}>
                  {availableSchedules.map(s => (
                    <option key={s.id} value={s.id}>
                      {s.course_name} - {s.full_name || ''} ({s.course_type === 'lab' ? 'LAB' : 'Theory'})
                    </option>
                  ))}
                </select>
              </div>

              <div className="radar-box">
                <div className="radar-header-row">
                  <span style={{ fontSize: 13, fontWeight: 800 }}>Geofence Simulation</span>
                  <span className="badge badge-success">Campus Valid</span>
                </div>
                <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                  Coordinates fixed to GL Bajaj Academic Block.
                </div>
              </div>

              {profResult && (
                <div className={`verify-result-box show ${profResult.status}`}>
                  <div className="verify-result-title">{profResult.title}</div>
                  <div>{profResult.message}</div>
                </div>
              )}
            </div>

            {/* Right: Camera */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
              <div className="camera-viewport">
                <video ref={profVideoRef} autoPlay playsInline muted />
                <div className="camera-reticle-overlay">
                  <div className="face-target-reticle">
                    <div className="radar-scan-line" />
                  </div>
                </div>
                {cameraBlocked && (
                  <div className="camera-blocked-fallback" style={{ display: 'flex' }}>
                    <AlertCircle size={40} />
                    <div>Camera access required.<br />Allow browser camera permissions.</div>
                  </div>
                )}
              </div>

              <button
                className="auth-btn danger"
                style={{ padding: 14, fontSize: 14 }}
                onClick={handleProfCheckin}
                disabled={profVerifying}
              >
                {profVerifying && <span className="btn-loader" />}
                <span>Capture &amp; Verify Student</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Hidden canvas for frame capture */}
      <canvas ref={canvasRef} style={{ display: 'none' }} />
    </div>
  );
}
