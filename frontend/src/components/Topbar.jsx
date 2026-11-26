import React from 'react';
import { LogOut } from 'lucide-react';

export default function Topbar({
  backendOnline,
  cameraActive,
  currentUser,
  onLogout
}) {
  const roleName = currentUser?.role === 'professor' ? 'Faculty: ' : 'Student: ';
  const secTag = currentUser?.section ? ` Sec-${currentUser.section}` : '';
  const groupTag = currentUser?.group ? ` (${currentUser.group})` : '';

  return (
    <header className="topbar">
      <div className="brand">
        <div className="brand-icon">GL</div>
        <div>
          <div className="brand-title">
            GLBAJAJ <span className="brand-sec-badge">SEC-H (ROOM 242)</span>
          </div>
          <div className="brand-sub">
            AI Attendance &amp; Lab Radar System &bull; Sem III 2026-27
          </div>
        </div>
      </div>

      <div className="topbar-right">
        <div className={`pill ${backendOnline ? 'online' : 'offline'}`} id="backendPill">
          <span className="dot"></span>
          <span>{backendOnline ? 'Backend Online' : 'Backend Offline'}</span>
        </div>

        <div className={`pill ${cameraActive ? 'cam-on' : 'offline'}`} id="cameraPill">
          <span className="dot"></span>
          <span>{cameraActive ? 'Camera Live' : 'Camera Off'}</span>
        </div>

        <div className={`user-badge-chip ${currentUser?.role || 'student'}`} id="topUserChip">
          <span className="role-indicator"></span>
          <span>
            {roleName}
            {currentUser?.name || 'User'}
            {secTag}
            {groupTag}
          </span>
        </div>

        <button className="logout-action-btn" onClick={onLogout} title="Sign Out">
          <LogOut size={14} style={{ display: 'inline', marginRight: 4, verticalAlign: 'middle' }} />
          Logout
        </button>
      </div>
    </header>
  );
}
