import React, { useState, useEffect } from 'react';
import { RefreshCw, CheckCircle, XCircle } from 'lucide-react';
import { API_BASE } from '../constants/scheduleData';

export default function ManageSessionsPanel({
  currentUser,
  availableSchedules,
  showToast,
  onSessionUpdated
}) {
  const [activeSessions, setActiveSessions] = useState([]);
  const [sessionHistory, setSessionHistory] = useState([]);
  const [loading, setLoading] = useState(false);
  const [actionLoadingId, setActionLoadingId] = useState(null);

  const fetchSessionData = async () => {
    setLoading(true);
    try {
      const [resActive, resHist] = await Promise.all([
        fetch(`${API_BASE}/sessions/active`),
        fetch(`${API_BASE}/sessions/history`)
      ]);
      const activeData = await resActive.json();
      const histData = await resHist.json();
      setActiveSessions(Array.isArray(activeData) ? activeData : []);
      setSessionHistory(Array.isArray(histData) ? histData : []);
    } catch (err) {
      console.warn('Error fetching session data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSessionData();
  }, []);

  const openSession = async (scheduleId) => {
    setActionLoadingId(scheduleId);
    try {
      const profId = currentUser?.id || 1;
      const res = await fetch(`${API_BASE}/sessions/open?schedule_id=${scheduleId}&prof_id=${profId}`, {
        method: 'POST'
      });
      const data = await res.json();
      showToast('success', data.message || 'Attendance session opened.');
      await fetchSessionData();
      onSessionUpdated?.();
    } catch (err) {
      showToast('error', 'Error: ' + err.message);
    } finally {
      setActionLoadingId(null);
    }
  };

  const closeSession = async (scheduleId) => {
    setActionLoadingId(scheduleId);
    try {
      const res = await fetch(`${API_BASE}/sessions/close?schedule_id=${scheduleId}`, {
        method: 'POST'
      });
      const data = await res.json();
      showToast('info', data.message || 'Attendance session closed.');
      await fetchSessionData();
      onSessionUpdated?.();
    } catch (err) {
      showToast('error', 'Error: ' + err.message);
    } finally {
      setActionLoadingId(null);
    }
  };

  const activeIds = new Set(activeSessions.map((a) => a.schedule_id));

  return (
    <div className="tab-panel active">
      {/* Banner */}
      <div className="page-hero-banner" style={{ background: 'linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%)' }}>
        <div>
          <div className="page-hero-title">Manage Attendance Sessions</div>
          <div className="page-hero-sub">
            Open attendance for particular classes or lab sessions. Students can ONLY check-in when open.
          </div>
          <div className="page-hero-tags">
            <span className="hero-tag">Faculty Access Level</span>
            <span className="hero-tag">Real-Time Geofence Activation</span>
          </div>
        </div>
        <button
          className="tt-filter-btn"
          style={{ background: '#fff', color: 'var(--success)', fontWeight: 800 }}
          onClick={fetchSessionData}
          disabled={loading}
        >
          <RefreshCw size={14} style={{ display: 'inline', marginRight: 6 }} />
          Refresh Sessions
        </button>
      </div>

      {/* Faculty Control Grid */}
      <div className="dashboard-card">
        <div className="card-head">
          <div>
            <div className="card-heading">Class &amp; Lab Attendance Controller</div>
            <div className="card-subheading">
              Click <strong>Open Attendance</strong> to allow students of that class/lab to mark attendance. Click <strong>Close</strong> when session ends.
            </div>
          </div>
        </div>

        <div className="faculty-control-grid">
          {availableSchedules.map((sched) => {
            const isOpen = activeIds.has(sched.id);
            const activeData = activeSessions.find((a) => a.schedule_id === sched.id);
            const isLab = sched.course_type === 'lab';
            const isActing = actionLoadingId === sched.id;

            return (
              <div
                key={sched.id}
                className={`faculty-class-card ${isOpen ? 'active-open' : ''}`}
              >
                <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 8 }}>
                  <div>
                    <div style={{ fontSize: 15, fontWeight: 800, color: 'var(--text)' }}>
                      {sched.course_name}
                    </div>
                    <div style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                      {sched.full_name || ''}
                    </div>
                  </div>
                  <span className={`badge ${isOpen ? 'badge-success' : 'badge-neutral'}`}>
                    {isOpen ? 'OPEN' : 'CLOSED'}
                  </span>
                </div>

                <div style={{ fontSize: 12, color: 'var(--text-muted)', display: 'flex', flexDirection: 'column', gap: 4 }}>
                  <div>
                    <strong>Type:</strong> {isLab ? 'Lab Session' : 'Theory'}
                  </div>
                  <div>
                    <strong>Location:</strong> {sched.room_or_lab || 'Room 242'}
                  </div>
                  <div>
                    <strong>Timing:</strong> {sched.time_slot || 'N/A'}
                  </div>
                  {sched.target_group && (
                    <div>
                      <strong>Batch:</strong> {sched.target_group}
                    </div>
                  )}
                  {isOpen && (
                    <div style={{ color: 'var(--success)', fontWeight: 700 }}>
                      Active since {activeData?.opened_at || ''}
                    </div>
                  )}
                </div>

                <div style={{ marginTop: 'auto', paddingTop: 10, borderTop: '1px solid var(--border)' }}>
                  {isOpen ? (
                    <button
                      className="auth-btn danger"
                      onClick={() => closeSession(sched.id)}
                      disabled={isActing}
                    >
                      {isActing && <span className="btn-loader"></span>}
                      Close Attendance
                    </button>
                  ) : (
                    <button
                      className="auth-btn success"
                      onClick={() => openSession(sched.id)}
                      disabled={isActing}
                    >
                      {isActing && <span className="btn-loader"></span>}
                      Open Attendance
                    </button>
                  )}
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Session History Audit Table */}
      <div className="dashboard-card" style={{ marginTop: 24 }}>
        <div className="card-head">
          <div>
            <div className="card-heading">Session History</div>
            <div className="card-subheading">Recent open/close logs for compliance and auditing</div>
          </div>
        </div>

        <div className="data-table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Class / Lab</th>
                <th>Opened By</th>
                <th>Opened At</th>
                <th>Closed At</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {sessionHistory.length === 0 ? (
                <tr>
                  <td colSpan={5} style={{ textAlign: 'center', padding: 24, color: 'var(--text-muted)' }}>
                    No sessions recorded yet.
                  </td>
                </tr>
              ) : (
                sessionHistory.map((r) => (
                  <tr key={r.session_id}>
                    <td><strong>{r.course_name}</strong></td>
                    <td>{r.opened_by_name || 'Faculty'}</td>
                    <td className="mono">{r.opened_at || '--'}</td>
                    <td className="mono">
                      {r.closed_at ? (
                        r.closed_at
                      ) : (
                        <span style={{ color: 'var(--success)', fontWeight: 700 }}>Still Open</span>
                      )}
                    </td>
                    <td>
                      <span className={`badge ${r.is_active === 'yes' ? 'badge-success' : 'badge-neutral'}`}>
                        {r.is_active === 'yes' ? 'Open' : 'Closed'}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
