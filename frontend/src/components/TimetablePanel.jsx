import React, { useState } from 'react';
import { User, MapPin, Clock, Users, Grid, BookOpen, FlaskConical } from 'lucide-react';

export default function TimetablePanel({ availableSchedules }) {
  const [filterCategory, setFilterCategory] = useState('all'); // 'all' | 'theory' | 'lab'
  const [showMatrix, setShowMatrix] = useState(false);

  const filteredList = availableSchedules.filter((item) => {
    if (filterCategory === 'theory') return item.course_type === 'theory';
    if (filterCategory === 'lab') return item.course_type === 'lab';
    return true;
  });

  return (
    <div className="tab-panel active">
      {/* Banner */}
      <div className="page-hero-banner" style={{ background: 'linear-gradient(135deg, var(--purple) 0%, #8E24AA 100%)' }}>
        <div>
          <div className="page-hero-title">Official Time Table &amp; Lab Schedules</div>
          <div className="page-hero-sub">
            GL Bajaj Group of Institutions &bull; Dept of CSE &bull; Odd Sem 2026-27 &bull; Sec: H &bull; Room: 242 (Block-B)
          </div>
          <div className="page-hero-tags">
            <span className="hero-tag">Branch: CSE-AIML &amp; CS</span>
            <span className="hero-tag">Class Coordinator: Er. Gopal Singh</span>
            <span className="hero-tag">HOD: Dr. Ravindra Kumar Vishwakarma</span>
          </div>
        </div>
      </div>

      {/* Filter Tabs */}
      <div className="tt-filter-tabs">
        <button
          className={`tt-filter-btn ${filterCategory === 'all' ? 'active' : ''}`}
          onClick={() => setFilterCategory('all')}
        >
          All Classes &amp; Labs
        </button>
        <button
          className={`tt-filter-btn ${filterCategory === 'theory' ? 'active' : ''}`}
          onClick={() => setFilterCategory('theory')}
        >
          Theory Classes (6)
        </button>
        <button
          className={`tt-filter-btn ${filterCategory === 'lab' ? 'active' : ''}`}
          onClick={() => setFilterCategory('lab')}
        >
          Lab Sessions (4)
        </button>
        <button
          className={`tt-filter-btn ${showMatrix ? 'active' : ''}`}
          onClick={() => setShowMatrix(!showMatrix)}
        >
          <Grid size={14} style={{ display: 'inline', marginRight: 4 }} />
          {showMatrix ? 'Hide Weekly Matrix' : 'View Weekly Matrix Grid'}
        </button>
      </div>

      {/* Weekly Matrix View */}
      {showMatrix && (
        <div className="timetable-table-wrap">
          <div style={{ padding: '16px 20px', background: '#f8fafc', borderBottom: '1.5px solid var(--border)', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <strong style={{ color: 'var(--primary)', fontSize: 14 }}>
              WEEKLY CLASS SCHEDULE MATRIX (SEC: H, ROOM 242)
            </strong>
            <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>w.e.f. 24.08.2026</span>
          </div>
          <table className="timetable-table">
            <thead>
              <tr>
                <th>Day</th>
                <th>09:10-10:00</th>
                <th>10:01-10:50</th>
                <th className="break-col">10:51-11:00</th>
                <th>11:01-11:50</th>
                <th>11:51-12:40</th>
                <th>12:41-01:30</th>
                <th className="lunch-col">01:31-02:20</th>
                <th>02:21-03:10</th>
                <th>03:11-04:00</th>
                <th>04:01-04:50</th>
              </tr>
            </thead>
            <tbody>
              {/* MON */}
              <tr>
                <td className="day-col">MON</td>
                <td><div className="tt-cell-item tt-cell-theory">PYTHON<span className="tt-cell-sub">Er. Bhanu Pratap</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">MATH-IV<span className="tt-cell-sub">Dr. Ashish Kumar</span></div></td>
                <td rowSpan={5} className="break-col">B R E A K</td>
                <td><div className="tt-cell-item tt-cell-theory">DS<span className="tt-cell-sub">Er. Richa Mishra</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">DSTL<span className="tt-cell-sub">Er. Gopal Singh</span></div></td>
                <td>--</td>
                <td rowSpan={5} className="lunch-col">L U N C H</td>
                <td colSpan={2}><div className="tt-cell-item" style={{ background: '#e0f2fe', color: '#0369a1', fontWeight: 700 }}>Technical Training</div></td>
                <td><div className="tt-cell-item" style={{ background: '#f1f5f9' }}>Library</div></td>
              </tr>
              {/* TUE */}
              <tr>
                <td className="day-col">TUE</td>
                <td><div className="tt-cell-item tt-cell-theory">MATH-IV<span className="tt-cell-sub">Dr. Ashish Kumar</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">DS<span className="tt-cell-sub">Er. Richa Mishra</span></div></td>
                <td colSpan={2}>
                  <div className="tt-cell-item tt-cell-lab">COA Lab (G2) Lab-07<span className="tt-cell-sub">Er. Hitendra</span></div>
                  <div className="tt-cell-item tt-cell-lab">WDW Lab (G1) Lab-11 (321)<span className="tt-cell-sub">Er. Gopal Singh</span></div>
                </td>
                <td><div className="tt-cell-item" style={{ background: '#f1f5f9' }}>Library</div></td>
                <td colSpan={2}><div className="tt-cell-item tt-cell-theory">COA<span className="tt-cell-sub">Er. Hitendra</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">UHV<span className="tt-cell-sub">Dr. Bablu Kumar</span></div></td>
              </tr>
              {/* WED */}
              <tr>
                <td className="day-col">WED</td>
                <td><div className="tt-cell-item tt-cell-theory">PYTHON<span className="tt-cell-sub">Er. Bhanu Pratap</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">DS<span className="tt-cell-sub">Er. Richa Mishra</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">COA<span className="tt-cell-sub">Er. Hitendra</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">DSTL<span className="tt-cell-sub">Er. Gopal Singh</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">MATH-IV<span className="tt-cell-sub">Dr. Ashish Kumar</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">UHV<span className="tt-cell-sub">Dr. Bablu Kumar</span></div></td>
                <td colSpan={2}>
                  <div className="tt-cell-item tt-cell-lab">DS Lab (G1) Lab-05<span className="tt-cell-sub">Er. Richa Mishra</span></div>
                  <div className="tt-cell-item tt-cell-lab">Mini Project (G2) Lab-06<span className="tt-cell-sub">Er. Gopal / Hitendra</span></div>
                </td>
              </tr>
              {/* THU */}
              <tr>
                <td className="day-col">THU</td>
                <td><div className="tt-cell-item tt-cell-theory">MATH-IV<span className="tt-cell-sub">Dr. Ashish Kumar</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">COA<span className="tt-cell-sub">Er. Hitendra</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">DS<span className="tt-cell-sub">Er. Richa Mishra</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">DSTL<span className="tt-cell-sub">Er. Gopal Singh</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">PYTHON<span className="tt-cell-sub">Er. Bhanu Pratap</span></div></td>
                <td colSpan={2}>
                  <div className="tt-cell-item tt-cell-lab">COA Lab (G1) Lab-03<span className="tt-cell-sub">Er. Hitendra</span></div>
                  <div className="tt-cell-item tt-cell-lab">WDW Lab (G2) Lab-04<span className="tt-cell-sub">Er. Gopal Singh</span></div>
                </td>
                <td><div className="tt-cell-item" style={{ background: '#f1f5f9' }}>Library</div></td>
              </tr>
              {/* FRI */}
              <tr>
                <td className="day-col">FRI</td>
                <td><div className="tt-cell-item tt-cell-theory">DSTL<span className="tt-cell-sub">Er. Gopal Singh</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">COA<span className="tt-cell-sub">Er. Hitendra</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">PYTHON<span className="tt-cell-sub">Er. Bhanu Pratap</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">MATH-IV<span className="tt-cell-sub">Dr. Ashish Kumar</span></div></td>
                <td><div className="tt-cell-item tt-cell-theory">DS<span className="tt-cell-sub">Er. Richa Mishra</span></div></td>
                <td colSpan={2}>
                  <div className="tt-cell-item tt-cell-lab">DS Lab (G2) Lab-05<span className="tt-cell-sub">Er. Richa Mishra</span></div>
                  <div className="tt-cell-item tt-cell-lab">Mini Project (G1) Lab-06<span className="tt-cell-sub">Er. Gopal / Hitendra</span></div>
                </td>
                <td><div className="tt-cell-item tt-cell-theory">UHV<span className="tt-cell-sub">Dr. Bablu Kumar</span></div></td>
              </tr>
            </tbody>
          </table>
        </div>
      )}

      {/* Cards Grid */}
      <div className="schedule-cards-grid">
        {filteredList.map((item) => {
          const isLab = item.course_type === 'lab';
          return (
            <div
              key={item.id}
              className={`schedule-item-card ${isLab ? 'is-lab' : 'is-theory'}`}
            >
              <div className="scard-header-row">
                <div
                  className="scard-icon-box"
                  style={{ background: item.color || '#003087', color: '#fff', fontSize: 18 }}
                >
                  {item.icon || (isLab ? '🔬' : '📘')}
                </div>
                <div>
                  <div className="scard-code-title">{item.course_name}</div>
                  <div className="scard-full-title">{item.full_name || ''}</div>
                </div>
              </div>

              <div className="scard-details-list">
                <div className="scard-detail-row">
                  <User size={15} />
                  <div>
                    <strong>Faculty:</strong> {item.faculty_name || 'Department Faculty'}
                  </div>
                </div>
                <div className="scard-detail-row">
                  <MapPin size={15} />
                  <div>
                    <strong>Location:</strong> {item.room_or_lab || 'Room 242'}
                  </div>
                </div>
                <div className="scard-detail-row">
                  <Clock size={15} />
                  <div>
                    <strong>Timing:</strong> {item.time_slot || 'As scheduled'}
                  </div>
                </div>
                {item.target_group && (
                  <div className="scard-detail-row">
                    <Users size={15} />
                    <div>
                      <strong>Group:</strong> {item.target_group}
                    </div>
                  </div>
                )}
              </div>

              <div className="scard-footer-row">
                <span className={`badge ${isLab ? 'badge-lab' : 'badge-theory'}`}>
                  {isLab ? 'Lab Session' : 'Theory Course'}
                </span>
                <span style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-muted)' }}>
                  Radius: {item.allowed_radius_m || 100}m
                </span>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
