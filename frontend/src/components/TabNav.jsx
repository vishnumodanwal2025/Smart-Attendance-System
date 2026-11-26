import React from 'react';
import { ShieldCheck, Clock, Camera, Calendar, FileText } from 'lucide-react';

export default function TabNav({ activeTab, setActiveTab }) {
  return (
    <nav className="tab-nav">
      <button
        className={`nav-tab-btn ${activeTab === 'checkin' ? 'active' : ''}`}
        id="tabBtn-checkin"
        onClick={() => setActiveTab('checkin')}
      >
        <ShieldCheck size={16} />
        Live Check-In
      </button>

      {/* Faculty-only tabs — shown/hidden via CSS: body.role-professor .faculty-only */}
      <button
        className={`nav-tab-btn faculty-only ${activeTab === 'sessions' ? 'active' : ''}`}
        id="tabBtn-sessions"
        onClick={() => setActiveTab('sessions')}
      >
        <Clock size={16} />
        Manage Attendance
      </button>

      <button
        className={`nav-tab-btn faculty-only ${activeTab === 'enroll' ? 'active' : ''}`}
        id="tabBtn-enroll"
        onClick={() => setActiveTab('enroll')}
      >
        <Camera size={16} />
        Face Enrollment
      </button>

      <button
        className={`nav-tab-btn ${activeTab === 'schedules' ? 'active' : ''}`}
        id="tabBtn-schedules"
        onClick={() => setActiveTab('schedules')}
      >
        <Calendar size={16} />
        Class Timetable &amp; Labs
      </button>

      <button
        className={`nav-tab-btn ${activeTab === 'history' ? 'active' : ''}`}
        id="tabBtn-history"
        onClick={() => setActiveTab('history')}
      >
        <FileText size={16} />
        Attendance Logs
      </button>
    </nav>
  );
}
