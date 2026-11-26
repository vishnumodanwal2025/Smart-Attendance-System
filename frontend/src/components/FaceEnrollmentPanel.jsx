import React, { useState, useRef, useEffect } from 'react';
import { Upload, Camera, RefreshCw } from 'lucide-react';
import { API_BASE } from '../constants/scheduleData';

export default function FaceEnrollmentPanel({
  enrolledStudents,
  onStudentEnrolled,
  showToast
}) {
  const [selectedStudentId, setSelectedStudentId] = useState('');
  const [internalId, setInternalId] = useState('1');
  const [enrollMode, setEnrollMode] = useState('upload'); // 'upload' | 'camera'

  const [selectedFile, setSelectedFile] = useState(null);
  const [capturedBlob, setCapturedBlob] = useState(null);
  const [previewUrl, setPreviewUrl] = useState('');
  const [loading, setLoading] = useState(false);
  const [resultBox, setResultBox] = useState(null); // { status, title, message }

  const videoRef = useRef(null);
  const streamRef = useRef(null);

  useEffect(() => {
    if (enrolledStudents.length > 0 && !selectedStudentId) {
      setSelectedStudentId(enrolledStudents[0].id);
      setInternalId(String(enrolledStudents[0].id));
    }
  }, [enrolledStudents]);

  const handleStudentChange = (id) => {
    setSelectedStudentId(id);
    setInternalId(String(id));
  };

  const startCamera = async () => {
    stopCamera();
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 640, height: 480, facingMode: 'user' }
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
    } catch (err) {
      showToast('error', 'Camera access blocked.');
    }
  };

  const stopCamera = () => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach((t) => t.stop());
      streamRef.current = null;
    }
  };

  useEffect(() => {
    if (enrollMode === 'camera') {
      startCamera();
    } else {
      stopCamera();
    }
    return () => stopCamera();
  }, [enrollMode]);

  const captureSnapshot = () => {
    const video = videoRef.current;
    if (!video) return;

    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth || 640;
    canvas.height = video.videoHeight || 480;
    const ctx = canvas.getContext('2d');
    if (ctx) {
      ctx.save();
      ctx.scale(-1, 1);
      ctx.drawImage(video, -canvas.width, 0, canvas.width, canvas.height);
      ctx.restore();
    }

    canvas.toBlob((blob) => {
      setCapturedBlob(blob);
      setPreviewUrl(URL.createObjectURL(blob));
      stopCamera();
    }, 'image/jpeg', 0.92);
  };

  const retakeSnapshot = () => {
    setCapturedBlob(null);
    setPreviewUrl('');
    startCamera();
  };

  const handleEnrollSubmit = async () => {
    setResultBox(null);
    const stuId = internalId || selectedStudentId;

    if (!stuId) {
      setResultBox({
        status: 'warning',
        title: 'Missing Student ID',
        message: 'Please specify student ID.'
      });
      return;
    }

    let fileToSend = null;
    if (enrollMode === 'camera') {
      if (!capturedBlob) {
        setResultBox({
          status: 'warning',
          title: 'No Photo',
          message: 'Capture camera snapshot first.'
        });
        return;
      }
      fileToSend = capturedBlob;
    } else {
      if (!selectedFile) {
        setResultBox({
          status: 'warning',
          title: 'No File Selected',
          message: 'Choose a face photo to upload.'
        });
        return;
      }
      fileToSend = selectedFile;
    }

    setLoading(true);
    const formData = new FormData();
    formData.append('file', fileToSend, 'face_baseline.jpg');

    try {
      const res = await fetch(`${API_BASE}/users/${stuId}/upload-face`, {
        method: 'POST',
        body: formData
      });
      const data = await res.json();
      setLoading(false);

      if (data.status === 'success') {
        setResultBox({
          status: 'success',
          title: 'Face Enrolled Successfully!',
          message: data.message
        });
        showToast('success', `Student #${stuId} baseline registered!`);
        onStudentEnrolled?.();
        if (enrollMode === 'camera') {
          retakeSnapshot();
        } else {
          setSelectedFile(null);
        }
      } else {
        setResultBox({
          status: 'error',
          title: 'Enrollment Failed',
          message: data.message || 'Face detection failed.'
        });
      }
    } catch (err) {
      setLoading(false);
      setResultBox({
        status: 'error',
        title: 'Network Error',
        message: err.message
      });
    }
  };

  return (
    <div className="tab-panel active">
      {/* Banner */}
      <div className="page-hero-banner" style={{ background: 'linear-gradient(135deg, var(--accent) 0%, #e74c3c 100%)' }}>
        <div>
          <div className="page-hero-title">Biometric Face Enrollment</div>
          <div className="page-hero-sub">
            Register baseline facial identity for students to enable AI face verification
          </div>
          <div className="page-hero-tags">
            <span className="hero-tag">Biometric Admin</span>
            <span className="hero-tag">Section H &bull; CSE-AIML &amp; CS</span>
          </div>
        </div>
      </div>

      <div style={{ maxWidth: 640, margin: '0 auto' }}>
        <div className="dashboard-card card-red">
          <div className="card-head">
            <div>
              <div className="card-heading">Register Student Face Baseline</div>
              <div className="card-subheading">
                Upload a clear passport photo or capture live through the camera
              </div>
            </div>
          </div>

          <div className="field-group">
            <label className="field-label">Select Student</label>
            <select
              className="field-select"
              value={selectedStudentId}
              onChange={(e) => handleStudentChange(e.target.value)}
            >
              {enrolledStudents.map((stu) => (
                <option key={stu.id} value={stu.id}>
                  {stu.name} {stu.enrollment_no ? `(${stu.enrollment_no})` : ''}
                  {stu.group ? ` - ${stu.group}` : ''}
                  {stu.has_face_encoding ? ' [Face Baseline]' : ' [No Face]'}
                </option>
              ))}
            </select>
          </div>

          <div className="field-group">
            <label className="field-label">Student ID (Internal Number)</label>
            <input
              className="field-input"
              type="number"
              value={internalId}
              min="1"
              onChange={(e) => setInternalId(e.target.value)}
            />
          </div>

          <div>
            <label className="field-label" style={{ display: 'block', marginBottom: 8 }}>
              Photo Capture Mode
            </label>
            <div className="role-selector">
              <button
                type="button"
                className={`role-btn ${enrollMode === 'upload' ? 'active' : ''}`}
                onClick={() => setEnrollMode('upload')}
              >
                <Upload size={16} />
                Upload Photo File
              </button>
              <button
                type="button"
                className={`role-btn ${enrollMode === 'camera' ? 'active' : ''}`}
                onClick={() => setEnrollMode('camera')}
              >
                <Camera size={16} />
                Live Camera Capture
              </button>
            </div>
          </div>

          {/* Mode 1: File Upload */}
          {enrollMode === 'upload' && (
            <div className="field-group" style={{ marginTop: 14 }}>
              <label className="field-label">Reference Face Photo (JPEG/PNG)</label>
              <input
                className="field-input"
                type="file"
                accept="image/*"
                onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
              />
            </div>
          )}

          {/* Mode 2: Camera Capture */}
          {enrollMode === 'camera' && (
            <div style={{ marginTop: 14 }}>
              {!capturedBlob ? (
                <div>
                  <div className="camera-viewport" style={{ maxHeight: 280 }}>
                    <video ref={videoRef} autoPlay playsInline muted></video>
                    <div className="camera-reticle-overlay">
                      <div className="face-target-reticle">
                        <div className="radar-scan-line"></div>
                      </div>
                    </div>
                  </div>
                  <button
                    className="auth-btn danger"
                    style={{ marginTop: 10 }}
                    onClick={captureSnapshot}
                  >
                    Capture Photo
                  </button>
                </div>
              ) : (
                <div>
                  <div
                    style={{
                      position: 'relative',
                      width: '100%',
                      aspectRatio: '4/3',
                      maxHeight: 280,
                      borderRadius: 'var(--radius-lg)',
                      overflow: 'hidden',
                      border: '2px solid var(--success)'
                    }}
                  >
                    <img
                      src={previewUrl}
                      alt="Captured Face"
                      style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                    />
                  </div>
                  <div style={{ display: 'flex', gap: 10, marginTop: 10 }}>
                    <button className="tt-filter-btn" style={{ flex: 1 }} onClick={retakeSnapshot}>
                      Retake Photo
                    </button>
                    <button
                      className="auth-btn success"
                      style={{ flex: 1 }}
                      onClick={handleEnrollSubmit}
                      disabled={loading}
                    >
                      {loading && <span className="btn-loader"></span>}
                      Use This Snapshot
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {enrollMode === 'upload' && (
            <div style={{ marginTop: 16 }}>
              <button
                className="auth-btn primary"
                onClick={handleEnrollSubmit}
                disabled={loading}
              >
                {loading && <span className="btn-loader"></span>}
                Enroll Face Reference
              </button>
            </div>
          )}

          {/* Result Alert Box */}
          {resultBox && (
            <div className={`verify-result-box show ${resultBox.status}`}>
              <div className="verify-result-title">{resultBox.title}</div>
              <div>{resultBox.message}</div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
