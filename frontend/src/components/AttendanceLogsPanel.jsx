import React, { useState } from 'react';
import { RefreshCw, Search } from 'lucide-react';

export default function AttendanceLogsPanel({
  attendanceLogs,
  loadingLogs,
  onRefreshLogs
}) {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('');

  const filteredLogs = attendanceLogs.filter((r) => {
    const sName = (r.student_name || '').toLowerCase();
    const cName = (r.course_name || '').toLowerCase();
    const q = searchQuery.toLowerCase().trim();
    const matchText = !q || sName.includes(q) || cName.includes(q);
    const matchStatus = !statusFilter || r.status === statusFilter;
    return matchText && matchStatus;
  });

  return (
    <div className="tab-panel active">
      {/* Banner */}
      <div className="page-hero-banner" style={{ background: 'linear-gradient(135deg, var(--teal) 0%, #004D40 100%)' }}>
        <div>
          <div className="page-hero-title">Attendance Records &amp; Logs</div>
          <div className="page-hero-sub">
            Complete audit record of attendance marked via face verification and geofence radar
          </div>
        </div>
        <button
          className="tt-filter-btn"
          style={{ background: '#fff', color: 'var(--teal)', fontWeight: 800 }}
          onClick={onRefreshLogs}
          disabled={loadingLogs}
        >
          <RefreshCw size={14} style={{ display: 'inline', marginRight: 6 }} />
          Refresh Logs
        </button>
      </div>

      <div className="dashboard-card">
        <div className="card-head">
          <div style={{ position: 'relative', flex: 1, maxWidth: 320 }}>
            <input
              className="field-input"
              type="search"
              placeholder="Search by student name or course..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>

          <select
            className="field-select"
            style={{ maxWidth: 180 }}
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
          >
            <option value="">All Statuses</option>
            <option value="Present">Present</option>
            <option value="Absent">Absent</option>
          </select>
        </div>

        <div className="data-table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Log ID</th>
                <th>Student</th>
                <th>Course / Lab</th>
                <th>Timestamp</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {loadingLogs ? (
                <tr>
                  <td colSpan={5} style={{ textAlign: 'center', padding: 24, color: 'var(--text-muted)' }}>
                    Loading logs...
                  </td>
                </tr>
              ) : filteredLogs.length === 0 ? (
                <tr>
                  <td colSpan={5} style={{ textAlign: 'center', padding: 24, color: 'var(--text-muted)' }}>
                    No attendance records found.
                  </td>
                </tr>
              ) : (
                filteredLogs.map((r) => (
                  <tr key={r.id}>
                    <td className="mono">#{r.id}</td>
                    <td>
                      <strong>{r.student_name}</strong>{' '}
                      <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>
                        (ID: {r.student_id})
                      </span>
                    </td>
                    <td>{r.course_name}</td>
                    <td className="mono">{r.timestamp || '--'}</td>
                    <td>
                      <span className={`badge ${r.status === 'Present' ? 'badge-success' : 'badge-warning'}`}>
                        {r.status}
                      </span>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>

        <div style={{ fontSize: 12, color: 'var(--text-muted)', textAlign: 'right', marginTop: 12 }}>
          {filteredLogs.length} record{filteredLogs.length !== 1 ? 's' : ''}
        </div>
      </div>
    </div>
  );
}
