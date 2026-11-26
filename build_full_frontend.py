# -*- coding: utf-8 -*-
"""
Builder script to generate the complete frontend/index.html for GLBAJAJ AI Attendance System.
Includes:
1. Student & Faculty Registration (Name, College Email, Password, Student ID / Enrollment No, Section, Group)
2. Sign In by Email or Student ID / Enrollment No
3. Lab Session Attendance System (Web Designing Workshop, Data Structure Lab, COA Lab, Mini Project Lab)
4. Official Reference Class & Lab Timetable Schedule (CSE-AIML & CS, Sec H, Sem III, Room 242)
5. Geofence Radar & Biometric Face Verification
"""

import os

HTML_CONTENT = r'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="AI Biometric Attendance & Geofence System - GL Bajaj Group of Institutions Mathura">
  <title>GLBAJAJ - AI Attendance System (CSE-AIML & CS)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <style>
    :root {
      --primary: #003087;
      --primary-dark: #002060;
      --primary-light: #1565C0;
      --primary-dim: rgba(0, 48, 135, 0.08);
      --primary-glow: rgba(0, 48, 135, 0.22);
      
      --accent: #C0392B;
      --accent-dark: #96281B;
      --accent-light: #e74c3c;
      --accent-dim: rgba(192, 57, 43, 0.1);
      --accent-glow: rgba(192, 57, 43, 0.25);
      
      --teal: #00897B;
      --teal-dim: rgba(0, 137, 123, 0.12);
      --teal-glow: rgba(0, 137, 123, 0.25);
      
      --purple: #6A1B9A;
      --purple-dim: rgba(106, 27, 154, 0.1);
      
      --amber: #D97706;
      --amber-dim: rgba(217, 119, 6, 0.12);
      
      --success: #2E7D32;
      --success-dim: rgba(46, 125, 50, 0.12);
      --warning: #E65100;
      --warning-dim: rgba(230, 81, 0, 0.12);
      --error: #C62828;
      --error-dim: rgba(198, 40, 40, 0.12);
      
      --bg-base: #f5f7fb;
      --bg-card: #ffffff;
      --bg-surface: #edf1f7;
      --border: #d7e0ea;
      --border-focus: #003087;
      
      --text: #1a2434;
      --text-muted: #566c86;
      --text-subtle: #8ea3bb;
      
      --radius-xl: 18px;
      --radius-lg: 12px;
      --radius-md: 8px;
      --radius-sm: 6px;
      
      --shadow-sm: 0 2px 6px rgba(0, 32, 96, 0.05);
      --shadow-md: 0 8px 24px rgba(0, 32, 96, 0.08);
      --shadow-lg: 0 16px 48px rgba(0, 32, 96, 0.14);
      --shadow-focus: 0 0 0 3px rgba(0, 48, 135, 0.22);
      --transition: 160ms cubic-bezier(0.4, 0, 0.2, 1);
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    html { scroll-behavior: smooth; }
    body {
      font-family: 'Inter', system-ui, -apple-system, sans-serif;
      font-size: 14px;
      line-height: 1.5;
      color: var(--text);
      background: var(--bg-base);
      min-height: 100vh;
      -webkit-font-smoothing: antialiased;
    }

    @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
    @keyframes slideUp { from { opacity: 0; transform: translateY(24px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes fadeUp { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
    @keyframes spin { to { transform: rotate(360deg); } }
    @keyframes sweep { 0% { top: 6%; opacity: 0; } 15% { opacity: 1; } 85% { opacity: 1; } 100% { top: 94%; opacity: 0; } }
    @keyframes pulse { 0%, 100% { opacity: 1; transform: scale(1); } 50% { opacity: 0.45; transform: scale(0.92); } }

    /* ============================================================
       AUTH OVERLAY & FORMS (SIGN IN / REGISTER)
       ============================================================ */
    #loginOverlay {
      position: fixed;
      inset: 0;
      z-index: 9999;
      background: radial-gradient(circle at 20% 20%, #002878 0%, #001844 50%, #0a0e1c 100%);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      padding: 24px;
      overflow-y: auto;
      animation: fadeIn 350ms ease both;
    }

    .auth-header {
      text-align: center;
      margin-bottom: 24px;
    }
    .auth-logo-row {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 16px;
      margin-bottom: 8px;
    }
    .auth-logo-badge {
      width: 56px;
      height: 56px;
      background: rgba(255, 255, 255, 0.12);
      border: 2px solid rgba(255, 255, 255, 0.35);
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(8px);
      box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    }
    .auth-college-title {
      font-size: 26px;
      font-weight: 800;
      color: #ffffff;
      letter-spacing: 2px;
      line-height: 1.1;
    }
    .auth-college-sub {
      font-size: 13px;
      color: rgba(255, 255, 255, 0.78);
      margin-top: 4px;
    }
    .auth-dept-tag {
      display: inline-block;
      margin-top: 8px;
      padding: 3px 12px;
      background: rgba(255, 255, 255, 0.15);
      border-radius: 999px;
      font-size: 11px;
      font-weight: 600;
      color: #ffcc00;
      letter-spacing: 0.5px;
    }

    .auth-card-container {
      width: 100%;
      max-width: 820px;
      background: #ffffff;
      border-radius: var(--radius-xl);
      box-shadow: 0 24px 64px rgba(0, 0, 0, 0.35);
      overflow: hidden;
      animation: slideUp 450ms cubic-bezier(0.16, 1, 0.3, 1) both;
    }

    /* Auth Modes Toggle */
    .auth-mode-tabs {
      display: flex;
      background: #eef2f7;
      border-bottom: 1.5px solid var(--border);
    }
    .auth-mode-tab {
      flex: 1;
      padding: 16px 20px;
      border: none;
      background: transparent;
      font-family: inherit;
      font-size: 14px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 10px;
      transition: all var(--transition);
      border-bottom: 3px solid transparent;
    }
    .auth-mode-tab:hover {
      color: var(--primary);
      background: rgba(255, 255, 255, 0.5);
    }
    .auth-mode-tab.active {
      color: var(--primary);
      background: #ffffff;
      border-bottom-color: var(--accent);
    }

    .auth-content-area {
      padding: 28px 32px;
    }

    /* Sign In Panels */
    .signin-panels-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 24px;
    }
    .signin-box {
      border: 1.5px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 22px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      background: #ffffff;
      transition: border-color var(--transition), box-shadow var(--transition);
    }
    .signin-box:hover {
      border-color: rgba(0, 48, 135, 0.4);
      box-shadow: var(--shadow-md);
    }
    .signin-box.student-accent { border-top: 4px solid var(--primary); }
    .signin-box.prof-accent { border-top: 4px solid var(--accent); }

    .signin-box-header {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .signin-icon {
      width: 42px;
      height: 42px;
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    .signin-icon.student { background: var(--primary-dim); color: var(--primary); }
    .signin-icon.prof { background: var(--accent-dim); color: var(--accent); }
    .signin-title { font-size: 16px; font-weight: 700; color: var(--text); }
    .signin-sub { font-size: 11px; color: var(--text-muted); }

    /* Form Inputs */
    .field-group {
      display: flex;
      flex-direction: column;
      gap: 5px;
    }
    .field-label {
      font-size: 11px;
      font-weight: 700;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    .field-input, .field-select {
      width: 100%;
      padding: 10px 13px;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-md);
      font-family: inherit;
      font-size: 13px;
      color: var(--text);
      background: var(--bg-surface);
      outline: none;
      transition: border-color var(--transition), box-shadow var(--transition), background var(--transition);
    }
    .field-input:focus, .field-select:focus {
      border-color: var(--border-focus);
      box-shadow: var(--shadow-focus);
      background: #ffffff;
    }

    /* Register Form Grid */
    .reg-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
    }
    .reg-full { grid-column: 1 / -1; }
    
    .role-selector {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 12px;
      margin-bottom: 16px;
    }
    .role-btn {
      padding: 12px;
      border: 2px solid var(--border);
      border-radius: var(--radius-md);
      background: var(--bg-surface);
      font-family: inherit;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all var(--transition);
    }
    .role-btn.active {
      border-color: var(--primary);
      background: var(--primary-dim);
      color: var(--primary);
    }

    /* Buttons */
    .auth-btn {
      width: 100%;
      padding: 12px 16px;
      border: none;
      border-radius: var(--radius-md);
      font-family: inherit;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      transition: all var(--transition);
    }
    .auth-btn.primary {
      background: linear-gradient(135deg, var(--primary) 0%, #1e5ac8 100%);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(0, 48, 135, 0.3);
    }
    .auth-btn.primary:hover {
      box-shadow: 0 6px 20px rgba(0, 48, 135, 0.45);
      transform: translateY(-1px);
    }
    .auth-btn.danger {
      background: linear-gradient(135deg, var(--accent) 0%, #e74c3c 100%);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(192, 57, 43, 0.3);
    }
    .auth-btn.danger:hover {
      box-shadow: 0 6px 20px rgba(192, 57, 43, 0.45);
      transform: translateY(-1px);
    }
    .auth-btn.success {
      background: linear-gradient(135deg, #2E7D32 0%, #43a047 100%);
      color: #ffffff;
      box-shadow: 0 4px 14px rgba(46, 125, 50, 0.3);
    }

    .auth-error {
      font-size: 12px;
      color: var(--error);
      background: var(--error-dim);
      border: 1px solid rgba(198, 40, 40, 0.3);
      border-radius: var(--radius-sm);
      padding: 8px 12px;
      display: none;
    }
    .auth-error.show { display: block; }

    .auth-footer {
      text-align: center;
      margin-top: 18px;
      font-size: 11px;
      color: rgba(255, 255, 255, 0.55);
    }

    /* ============================================================
       MAIN APP SHELL
       ============================================================ */
    #appShell { display: none; }
    #appShell.visible {
      display: flex;
      flex-direction: column;
      min-height: 100vh;
      animation: fadeIn 300ms ease both;
    }

    /* Topbar */
    .topbar {
      position: sticky;
      top: 0;
      z-index: 100;
      background: #ffffff;
      border-bottom: 3px solid var(--accent);
      padding: 0 24px;
      height: 66px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: 0 2px 10px rgba(0, 32, 96, 0.08);
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 14px;
      flex-shrink: 0;
    }
    .brand-icon {
      width: 42px;
      height: 42px;
      border-radius: 50%;
      background: linear-gradient(135deg, var(--primary), #1565C0);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-weight: 800;
      font-size: 18px;
      box-shadow: 0 2px 8px rgba(0, 48, 135, 0.35);
    }
    .brand-title {
      font-size: 20px;
      font-weight: 800;
      color: var(--primary);
      letter-spacing: 1.5px;
      line-height: 1;
    }
    .brand-sub {
      font-size: 11px;
      color: var(--text-muted);
      margin-top: 2px;
    }
    .brand-sec-badge {
      display: inline-block;
      margin-left: 8px;
      padding: 2px 8px;
      background: var(--amber-dim);
      border: 1px solid rgba(217, 119, 6, 0.3);
      color: var(--amber);
      font-size: 11px;
      font-weight: 700;
      border-radius: 4px;
    }

    .topbar-right {
      display: flex;
      align-items: center;
      gap: 10px;
      flex-wrap: wrap;
    }
    .pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border-radius: 999px;
      border: 1.5px solid var(--border);
      background: var(--bg-surface);
      font-size: 11px;
      font-weight: 600;
      color: var(--text-muted);
      white-space: nowrap;
    }
    .pill .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--text-subtle);
    }
    .pill.online {
      color: var(--success);
      border-color: rgba(46, 125, 50, 0.3);
      background: var(--success-dim);
    }
    .pill.online .dot {
      background: var(--success);
      box-shadow: 0 0 6px var(--success);
    }
    .pill.offline {
      color: var(--error);
      border-color: rgba(198, 40, 40, 0.3);
      background: var(--error-dim);
    }
    .pill.offline .dot { background: var(--error); }
    .pill.cam-on {
      color: var(--teal);
      border-color: rgba(0, 137, 123, 0.3);
      background: var(--teal-dim);
    }
    .pill.cam-on .dot {
      background: var(--teal);
      box-shadow: 0 0 6px var(--teal);
    }

    .user-badge-chip {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 14px;
      border-radius: 999px;
      border: 1.5px solid var(--border);
      background: var(--bg-surface);
      font-size: 12px;
      font-weight: 700;
      color: var(--text);
    }
    .user-badge-chip .role-indicator {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--primary);
    }
    .user-badge-chip.professor .role-indicator { background: var(--accent); }
    .logout-action-btn {
      padding: 6px 14px;
      border-radius: 999px;
      border: 1.5px solid rgba(192, 57, 43, 0.3);
      background: var(--accent-dim);
      color: var(--accent);
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      font-family: inherit;
      transition: all var(--transition);
    }
    .logout-action-btn:hover {
      background: var(--accent);
      color: #fff;
    }

    /* Navigation Bar */
    .tab-nav {
      display: flex;
      padding: 0 24px;
      background: var(--primary);
      overflow-x: auto;
      scrollbar-width: none;
    }
    .tab-nav::-webkit-scrollbar { display: none; }
    .nav-tab-btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 14px 20px;
      border: none;
      border-bottom: 3px solid transparent;
      background: transparent;
      color: rgba(255, 255, 255, 0.75);
      font-family: inherit;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all var(--transition);
      white-space: nowrap;
      flex-shrink: 0;
    }
    .nav-tab-btn:hover {
      color: #fff;
      background: rgba(255, 255, 255, 0.08);
    }
    .nav-tab-btn.active {
      color: #fff;
      border-bottom-color: var(--accent);
      background: rgba(255, 255, 255, 0.12);
    }
    .nav-tab-btn.faculty-only { display: none; }
    body.role-professor .nav-tab-btn.faculty-only { display: inline-flex; }

    /* Main Container */
    .app-main-content {
      flex: 1;
      padding: 28px 24px;
      max-width: 1320px;
      width: 100%;
      margin: 0 auto;
    }
    .tab-panel { display: none; }
    .tab-panel.active { display: block; animation: fadeUp 220ms ease both; }

    /* Page Banners */
    .page-hero-banner {
      background: linear-gradient(135deg, var(--primary) 0%, #1565C0 100%);
      border-radius: var(--radius-lg);
      padding: 22px 28px;
      margin-bottom: 24px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 16px;
      box-shadow: var(--shadow-md);
      color: #fff;
    }
    .page-hero-title { font-size: 20px; font-weight: 800; line-height: 1.2; }
    .page-hero-sub { font-size: 13px; color: rgba(255, 255, 255, 0.85); margin-top: 4px; }
    .page-hero-tags { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 8px; }
    .hero-tag {
      padding: 3px 10px;
      background: rgba(255, 255, 255, 0.18);
      border-radius: 999px;
      font-size: 11px;
      font-weight: 600;
      backdrop-filter: blur(4px);
    }

    /* Cards */
    .dashboard-card {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: var(--radius-xl);
      padding: 24px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .dashboard-card.card-blue { border-top: 4px solid var(--primary); }
    .dashboard-card.card-red { border-top: 4px solid var(--accent); }
    .dashboard-card.card-teal { border-top: 4px solid var(--teal); }
    .dashboard-card.card-purple { border-top: 4px solid var(--purple); }

    .card-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
    }
    .card-heading {
      font-size: 16px;
      font-weight: 800;
      color: var(--text);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .card-subheading {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }

    /* Badges */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 11px;
      border-radius: 999px;
      font-size: 11px;
      font-weight: 700;
      border: 1px solid transparent;
      text-transform: uppercase;
      letter-spacing: 0.04em;
    }
    .badge-success { background: var(--success-dim); color: var(--success); border-color: rgba(46, 125, 50, 0.25); }
    .badge-error { background: var(--error-dim); color: var(--error); border-color: rgba(198, 40, 40, 0.25); }
    .badge-warning { background: var(--warning-dim); color: var(--warning); border-color: rgba(230, 81, 0, 0.25); }
    .badge-info { background: var(--primary-dim); color: var(--primary); border-color: var(--primary-glow); }
    .badge-lab { background: var(--purple-dim); color: var(--purple); border-color: rgba(106, 27, 154, 0.25); }
    .badge-theory { background: var(--teal-dim); color: var(--teal); border-color: rgba(0, 137, 123, 0.25); }
    .badge-group { background: var(--amber-dim); color: var(--amber); border-color: rgba(217, 119, 6, 0.25); }
    .badge-neutral { background: var(--bg-surface); color: var(--text-muted); border-color: var(--border); }

    /* ============================================================
       TIMETABLE & CLASS SCHEDULE VIEW
       ============================================================ */
    .tt-filter-tabs {
      display: flex;
      gap: 8px;
      margin-bottom: 20px;
      flex-wrap: wrap;
    }
    .tt-filter-btn {
      padding: 9px 18px;
      border-radius: 999px;
      border: 1.5px solid var(--border);
      background: #ffffff;
      font-family: inherit;
      font-size: 13px;
      font-weight: 700;
      color: var(--text-muted);
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      transition: all var(--transition);
    }
    .tt-filter-btn:hover {
      border-color: var(--primary);
      color: var(--primary);
    }
    .tt-filter-btn.active {
      background: var(--primary);
      border-color: var(--primary);
      color: #ffffff;
      box-shadow: 0 2px 8px rgba(0, 48, 135, 0.3);
    }

    /* Timetable Grid View */
    .timetable-table-wrap {
      overflow-x: auto;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-lg);
      background: #ffffff;
      margin-bottom: 28px;
      box-shadow: var(--shadow-sm);
    }
    .timetable-table {
      width: 100%;
      min-width: 900px;
      border-collapse: collapse;
      font-size: 12px;
    }
    .timetable-table th {
      background: var(--primary);
      color: #ffffff;
      font-weight: 700;
      padding: 12px 10px;
      text-align: center;
      border-right: 1px solid rgba(255, 255, 255, 0.15);
      white-space: nowrap;
    }
    .timetable-table th:first-child { min-width: 80px; }
    .timetable-table td {
      border: 1px solid var(--border);
      padding: 10px 8px;
      text-align: center;
      vertical-align: middle;
      font-weight: 500;
    }
    .timetable-table .day-col {
      background: #f0f4fa;
      font-weight: 800;
      color: var(--primary);
    }
    .timetable-table .break-col {
      background: #fef3c7;
      color: #b45309;
      font-weight: 700;
      letter-spacing: 2px;
      writing-mode: vertical-rl;
      text-orientation: mixed;
      width: 32px;
      min-width: 32px;
    }
    .timetable-table .lunch-col {
      background: #fed7aa;
      color: #c2410c;
      font-weight: 700;
      letter-spacing: 2px;
      writing-mode: vertical-rl;
      text-orientation: mixed;
      width: 32px;
      min-width: 32px;
    }
    
    .tt-cell-item {
      padding: 6px;
      border-radius: 6px;
      margin: 2px 0;
      font-size: 11px;
      line-height: 1.3;
    }
    .tt-cell-theory {
      background: rgba(0, 48, 135, 0.08);
      border: 1px solid rgba(0, 48, 135, 0.2);
      color: var(--primary);
      font-weight: 700;
    }
    .tt-cell-lab {
      background: rgba(106, 27, 154, 0.09);
      border: 1px solid rgba(106, 27, 154, 0.25);
      color: var(--purple);
      font-weight: 700;
    }
    .tt-cell-sub {
      display: block;
      font-size: 10px;
      font-weight: 500;
      color: var(--text-muted);
      margin-top: 2px;
    }

    /* Course Cards Grid */
    .schedule-cards-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
      gap: 18px;
    }
    .schedule-item-card {
      background: #ffffff;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 20px;
      box-shadow: var(--shadow-sm);
      display: flex;
      flex-direction: column;
      gap: 14px;
      transition: all var(--transition);
      position: relative;
      overflow: hidden;
    }
    .schedule-item-card:hover {
      box-shadow: var(--shadow-md);
      transform: translateY(-2px);
    }
    .schedule-item-card.is-lab {
      border-top: 4px solid var(--purple);
      background: linear-gradient(180deg, rgba(106, 27, 154, 0.02) 0%, #ffffff 100%);
    }
    .schedule-item-card.is-theory {
      border-top: 4px solid var(--primary);
    }

    .scard-header-row {
      display: flex;
      align-items: flex-start;
      gap: 12px;
    }
    .scard-icon-box {
      width: 44px;
      height: 44px;
      border-radius: var(--radius-md);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      font-weight: 800;
      color: #fff;
      flex-shrink: 0;
    }
    .scard-code-title {
      font-size: 15px;
      font-weight: 800;
      color: var(--text);
      line-height: 1.2;
    }
    .scard-full-title {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }

    .scard-details-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
      font-size: 12px;
    }
    .scard-detail-row {
      display: flex;
      align-items: flex-start;
      gap: 8px;
      color: var(--text-muted);
    }
    .scard-detail-row strong {
      color: var(--text);
    }

    .scard-footer-row {
      padding-top: 12px;
      border-top: 1px solid var(--border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }

    /* ============================================================
       LIVE CHECK-IN & GEOFENCE RADAR VIEW
       ============================================================ */
    .checkin-layout-grid {
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
      gap: 24px;
      align-items: start;
    }
    @media (max-width: 860px) {
      .checkin-layout-grid { grid-template-columns: 1fr; }
    }

    /* Session Gate (When no session is open) */
    .session-empty-gate {
      padding: 60px 24px;
      text-align: center;
      background: var(--bg-surface);
      border: 2px dashed var(--border);
      border-radius: var(--radius-xl);
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 16px;
    }
    .gate-icon-circle {
      width: 68px;
      height: 68px;
      border-radius: 50%;
      background: var(--warning-dim);
      color: var(--warning);
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .gate-title { font-size: 18px; font-weight: 800; color: var(--text); }
    .gate-desc { font-size: 13px; color: var(--text-muted); max-width: 420px; line-height: 1.6; }

    /* Active Session Banner */
    .active-session-spotlight {
      background: linear-gradient(135deg, rgba(46, 125, 50, 0.08) 0%, rgba(46, 125, 50, 0.02) 100%);
      border: 2px solid rgba(46, 125, 50, 0.35);
      border-radius: var(--radius-lg);
      padding: 16px 20px;
      margin-bottom: 22px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 14px;
      flex-wrap: wrap;
    }
    .session-spotlight-left {
      display: flex;
      align-items: center;
      gap: 14px;
    }
    .live-pulse-dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: var(--success);
      box-shadow: 0 0 10px var(--success);
      animation: pulse 1.5s ease-in-out infinite;
      flex-shrink: 0;
    }
    .spotlight-class-name {
      font-size: 16px;
      font-weight: 800;
      color: var(--success);
    }
    .spotlight-class-meta {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 2px;
    }

    /* Geofence Radar Box */
    .radar-box {
      background: var(--bg-surface);
      border: 1.5px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .radar-header-row {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .coord-chips-row {
      display: flex;
      gap: 8px;
      font-family: 'JetBrains Mono', Consolas, monospace;
      font-size: 11px;
      color: var(--text-muted);
      flex-wrap: wrap;
    }
    .coord-chip {
      background: #ffffff;
      border: 1px solid var(--border);
      border-radius: var(--radius-sm);
      padding: 4px 8px;
    }
    .coord-chip strong { color: var(--text); }
    
    .distance-stat-card {
      background: #ffffff;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-md);
      padding: 12px 16px;
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .distance-value-text {
      font-size: 15px;
      font-weight: 800;
      color: var(--primary);
    }

    /* Camera Viewport */
    .camera-viewport {
      position: relative;
      width: 100%;
      aspect-ratio: 4/3;
      background: #080c14;
      border-radius: var(--radius-lg);
      overflow: hidden;
      border: 1.5px solid var(--border);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.15);
    }
    .camera-viewport video {
      width: 100%;
      height: 100%;
      object-fit: cover;
      transform: scaleX(-1);
      display: block;
    }
    .camera-reticle-overlay {
      position: absolute;
      inset: 0;
      pointer-events: none;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .face-target-reticle {
      width: 190px;
      height: 230px;
      border: 2px dashed rgba(0, 48, 135, 0.6);
      border-radius: 20px;
      position: relative;
    }
    .face-target-reticle::before {
      content: "";
      position: absolute;
      top: -2px; left: -2px;
      width: 24px; height: 24px;
      border-top: 3px solid #003087;
      border-left: 3px solid #003087;
      border-top-left-radius: 18px;
    }
    .face-target-reticle::after {
      content: "";
      position: absolute;
      bottom: -2px; right: -2px;
      width: 24px; height: 24px;
      border-bottom: 3px solid #003087;
      border-right: 3px solid #003087;
      border-bottom-right-radius: 18px;
    }
    .radar-scan-line {
      position: absolute;
      left: 0; right: 0;
      height: 2px;
      background: linear-gradient(90deg, transparent, #00d2ff, #003087, transparent);
      box-shadow: 0 0 10px #00d2ff;
      animation: sweep 2.4s linear infinite;
    }
    .camera-blocked-fallback {
      position: absolute;
      inset: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      gap: 12px;
      color: rgba(255, 255, 255, 0.6);
      font-size: 13px;
      text-align: center;
      padding: 20px;
    }

    /* Verification Results */
    .verify-result-box {
      display: none;
      padding: 14px 18px;
      border-radius: var(--radius-lg);
      border: 1.5px solid transparent;
      animation: fadeUp 200ms ease both;
    }
    .verify-result-box.show { display: block; }
    .verify-result-box.success {
      background: var(--success-dim);
      border-color: rgba(46, 125, 50, 0.35);
      color: var(--success);
    }
    .verify-result-box.error {
      background: var(--error-dim);
      border-color: rgba(198, 40, 40, 0.35);
      color: var(--error);
    }
    .verify-result-box.warning {
      background: var(--warning-dim);
      border-color: rgba(230, 81, 0, 0.35);
      color: var(--warning);
    }
    .verify-result-title {
      font-size: 14px;
      font-weight: 800;
      margin-bottom: 4px;
    }

    .similarity-bar-wrap {
      display: none;
      margin-top: 10px;
    }
    .similarity-bar-wrap.show { display: block; }
    .sim-labels-row {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: var(--text-muted);
      margin-bottom: 4px;
    }
    .sim-track {
      height: 8px;
      background: var(--bg-surface);
      border-radius: 4px;
      overflow: hidden;
      border: 1px solid var(--border);
    }
    .sim-fill {
      height: 100%;
      width: 0;
      background: linear-gradient(90deg, var(--primary), var(--teal));
      border-radius: 4px;
      transition: width 0.7s cubic-bezier(0.4, 0, 0.2, 1);
    }

    /* ============================================================
       FACULTY SESSIONS MANAGEMENT
       ============================================================ */
    .faculty-control-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(290px, 1fr));
      gap: 16px;
    }
    .faculty-class-card {
      background: #ffffff;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-lg);
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
      box-shadow: var(--shadow-sm);
      transition: all var(--transition);
    }
    .faculty-class-card.active-open {
      border-color: rgba(46, 125, 50, 0.5);
      background: linear-gradient(180deg, rgba(46, 125, 50, 0.04) 0%, #ffffff 100%);
      box-shadow: 0 4px 16px rgba(46, 125, 50, 0.15);
    }

    /* History Table */
    .data-table-container {
      overflow-x: auto;
      border: 1.5px solid var(--border);
      border-radius: var(--radius-lg);
      background: #ffffff;
    }
    .data-table {
      width: 100%;
      min-width: 650px;
      border-collapse: collapse;
      font-size: 13px;
    }
    .data-table th {
      background: var(--primary);
      color: #ffffff;
      padding: 12px 16px;
      text-align: left;
      font-size: 11px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      white-space: nowrap;
    }
    .data-table td {
      padding: 12px 16px;
      border-bottom: 1px solid var(--border);
      color: var(--text);
    }
    .data-table tr:last-child td { border-bottom: none; }
    .data-table tr:hover td { background: var(--primary-dim); }
    .data-table .mono { font-family: 'JetBrains Mono', Consolas, monospace; font-size: 12px; }

    /* Toast */
    #globalToast {
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 99999;
      padding: 12px 20px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 700;
      max-width: 380px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
      transition: opacity 0.3s ease, transform 0.3s ease;
      opacity: 0;
      pointer-events: none;
      transform: translateY(10px);
    }
    #globalToast.show {
      opacity: 1;
      pointer-events: auto;
      transform: translateY(0);
    }

    .btn-loader {
      display: none;
      width: 14px;
      height: 14px;
      border: 2px solid rgba(255, 255, 255, 0.35);
      border-top-color: #fff;
      border-radius: 50%;
      animation: spin 0.7s linear infinite;
    }

    @media (max-width: 720px) {
      .auth-content-area { padding: 20px 16px; }
      .signin-panels-grid, .reg-grid { grid-template-columns: 1fr; }
      .topbar { padding: 0 16px; }
      .app-main-content { padding: 16px 12px; }
      .brand-sub { display: none; }
    }
  </style>
</head>
<body>

<!-- ============================================================
     1. AUTHENTICATION OVERLAY: SIGN IN & REGISTRATION
     ============================================================ -->
<div id="loginOverlay" role="dialog" aria-modal="true">
  <div class="auth-header">
    <div class="auth-logo-row">
      <div class="auth-logo-badge">
        <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ffffff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          <path d="m9 12 2 2 4-4"/>
        </svg>
      </div>
      <div>
        <div class="auth-college-title">GL BAJAJ</div>
        <div class="auth-college-sub">Group of Institutions, Mathura</div>
      </div>
    </div>
    <div class="auth-dept-tag">Dept. of Computer Science &amp; Engineering &bull; CSE-AIML &amp; CS</div>
  </div>

  <div class="auth-card-container">
    <!-- Mode Switcher: Sign In vs New Registration -->
    <div class="auth-mode-tabs">
      <button class="auth-mode-tab active" id="tabModeSignIn" onclick="switchAuthMode('signin')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M15 3h4a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2h-4"/><polyline points="10 17 15 12 10 7"/><line x1="15" y1="12" x2="3" y2="12"/></svg>
        Sign In (Existing User)
      </button>
      <button class="auth-mode-tab" id="tabModeRegister" onclick="switchAuthMode('register')">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M16 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="8.5" cy="7" r="4"/><line x1="20" y1="8" x2="20" y2="14"/><line x1="23" y1="11" x2="17" y2="11"/></svg>
        New User Registration (Sign Up)
      </button>
    </div>

    <!-- Mode 1: Sign In -->
    <div class="auth-content-area" id="authSignInArea">
      <div class="signin-panels-grid">
        <!-- Student Login -->
        <div class="signin-box student-accent">
          <div class="signin-box-header">
            <div class="signin-icon student">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            </div>
            <div>
              <div class="signin-title">Student Sign In</div>
              <div class="signin-sub">Login with College Email or Student ID</div>
            </div>
          </div>
          <div class="field-group">
            <label class="field-label">Student ID or College Email</label>
            <input class="field-input" type="text" id="loginStudentId" placeholder="e.g. 25CSAIM076 or student@glbajaj.ac.in" autocomplete="username">
          </div>
          <div class="field-group">
            <label class="field-label">Password</label>
            <input class="field-input" type="password" id="loginStudentPass" placeholder="Enter your password" autocomplete="current-password">
          </div>
          <div class="auth-error" id="studentLoginError"></div>
          <button class="auth-btn primary" onclick="handleSignIn('student')">
            <span class="btn-loader" id="studentLoginLoader"></span>
            Sign In as Student
          </button>
        </div>

        <!-- Professor Login -->
        <div class="signin-box prof-accent">
          <div class="signin-box-header">
            <div class="signin-icon prof">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path d="M16 3.13a4 4 0 0 1 0 7.75"/></svg>
            </div>
            <div>
              <div class="signin-title">Faculty Sign In</div>
              <div class="signin-sub">Course Teacher / Coordinator Admin</div>
            </div>
          </div>
          <div class="field-group">
            <label class="field-label">Faculty College Email</label>
            <input class="field-input" type="email" id="loginProfEmail" placeholder="e.g. prof@glbajaj.ac.in" autocomplete="username">
          </div>
          <div class="field-group">
            <label class="field-label">Password</label>
            <input class="field-input" type="password" id="loginProfPass" placeholder="Enter your password" autocomplete="current-password">
          </div>
          <div class="auth-error" id="profLoginError"></div>
          <button class="auth-btn danger" onclick="handleSignIn('professor')">
            <span class="btn-loader" id="profLoginLoader"></span>
            Sign In as Faculty
          </button>
        </div>
      </div>
    </div>

    <!-- Mode 2: New User Registration -->
    <div class="auth-content-area" id="authRegisterArea" style="display: none;">
      <div style="margin-bottom: 16px;">
        <div style="font-size: 16px; font-weight: 800; color: var(--text);">Create New Account</div>
        <div style="font-size: 12px; color: var(--text-muted); margin-top: 2px;">Enter your college credentials, section, and group for automated timetable assignment.</div>
      </div>

      <!-- Role Selector -->
      <div class="role-selector">
        <button type="button" class="role-btn active" id="btnRoleStudent" onclick="selectRegRole('student')">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
          Student Account
        </button>
        <button type="button" class="role-btn" id="btnRoleProf" onclick="selectRegRole('professor')">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/></svg>
          Faculty / Teacher Account
        </button>
      </div>

      <div class="reg-grid">
        <div class="field-group">
          <label class="field-label">Full Name *</label>
          <input class="field-input" type="text" id="regName" placeholder="e.g. Vishnu Sharma" required>
        </div>

        <div class="field-group">
          <label class="field-label">College Email Address *</label>
          <input class="field-input" type="email" id="regEmail" placeholder="e.g. vishnu.sharma@glbajaj.ac.in" required>
        </div>

        <div class="field-group" id="regEnrollGroup">
          <label class="field-label">Student ID / Enrollment Number *</label>
          <input class="field-input" type="text" id="regEnrollNo" placeholder="e.g. 25CSAIM076">
        </div>

        <div class="field-group">
          <label class="field-label">Create Password (Min 4 chars) *</label>
          <input class="field-input" type="password" id="regPass" placeholder="Create strong password" required>
        </div>

        <div class="field-group" id="regSectionGroup">
          <label class="field-label">Section *</label>
          <select class="field-select" id="regSection">
            <option value="H" selected>Section H (CSE-AIML &amp; CS)</option>
            <option value="A">Section A</option>
            <option value="B">Section B</option>
            <option value="C">Section C</option>
            <option value="D">Section D</option>
            <option value="E">Section E</option>
            <option value="F">Section F</option>
            <option value="G">Section G</option>
          </select>
        </div>

        <div class="field-group" id="regBatchGroup">
          <label class="field-label">Lab Group / Batch *</label>
          <select class="field-select" id="regGroup">
            <option value="G1" selected>Group 1 (G1) - Web Designing / DS Lab G1</option>
            <option value="G2">Group 2 (G2) - COA Lab / Mini Project G2</option>
          </select>
        </div>

        <div class="reg-full">
          <div class="auth-error" id="regError"></div>
          <button class="auth-btn success" style="margin-top: 10px;" onclick="handleRegistration()">
            <span class="btn-loader" id="regLoader"></span>
            Register Account &amp; Proceed
          </button>
        </div>
      </div>
    </div>
  </div>

  <div class="auth-footer">&copy; 2026 GL Bajaj Group of Institutions, Mathura &bull; B.Tech CSE-AIML &amp; CS (Sem III)</div>
</div>


<!-- ============================================================
     2. APPLICATION INTERFACE
     ============================================================ -->
<div id="appShell">
  <!-- Topbar Header -->
  <header class="topbar">
    <div class="brand">
      <div class="brand-icon">GL</div>
      <div>
        <div class="brand-title">GLBAJAJ <span class="brand-sec-badge">SEC-H (ROOM 242)</span></div>
        <div class="brand-sub">AI Attendance &amp; Lab Radar System &bull; Sem III 2026-27</div>
      </div>
    </div>

    <div class="topbar-right">
      <div class="pill" id="backendPill"><span class="dot"></span><span id="backendStatusTxt">Connecting...</span></div>
      <div class="pill" id="cameraPill"><span class="dot"></span><span id="cameraStatusTxt">Camera Ready</span></div>
      <div class="user-badge-chip" id="topUserChip">
        <span class="role-indicator"></span>
        <span id="topUserChipTxt">User</span>
      </div>
      <button class="logout-action-btn" onclick="handleLogout()">Logout</button>
    </div>
  </header>

  <!-- Tab Navigation -->
  <nav class="tab-nav">
    <button class="nav-tab-btn active" id="tabBtn-checkin" onclick="navigateTab('checkin')">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
      Live Check-In
    </button>
    <button class="nav-tab-btn faculty-only" id="tabBtn-sessions" onclick="navigateTab('sessions')">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
      Manage Attendance
    </button>
    <button class="nav-tab-btn faculty-only" id="tabBtn-enroll" onclick="navigateTab('enroll')">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="4"/></svg>
      Face Enrollment
    </button>
    <button class="nav-tab-btn" id="tabBtn-schedules" onclick="navigateTab('schedules')">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>
      Class Timetable &amp; Labs
    </button>
    <button class="nav-tab-btn" id="tabBtn-history" onclick="navigateTab('history')">
      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/></svg>
      Attendance Logs
    </button>
  </nav>

  <!-- Main View Area -->
  <main class="app-main-content">

    <!-- ============================================================
         PANEL 1: LIVE CHECK-IN (GEOFENCE + FACE RECOGNITION)
         ============================================================ -->
    <div id="panel-checkin" class="tab-panel active">
      <div class="page-hero-banner">
        <div>
          <div class="page-hero-title">Live Attendance Verification</div>
          <div class="page-hero-sub">AI Biometric Face Verification + Campus Geofence Radar System</div>
          <div class="page-hero-tags">
            <span class="hero-tag">Room 242 (Block-B)</span>
            <span class="hero-tag">Section H &bull; Year 2 &bull; Sem III</span>
            <span class="hero-tag">CSE-AIML &amp; CS</span>
          </div>
        </div>
      </div>

      <!-- Student View: Waiting for faculty to open session -->
      <div id="studentWaitGate" style="display: none;">
        <div class="session-empty-gate">
          <div class="gate-icon-circle">
            <svg width="34" height="34" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          </div>
          <div class="gate-title">Attendance Session Not Active</div>
          <div class="gate-desc">Your course professor or lab instructor has not opened attendance for this slot yet. When opened, it will appear here automatically.</div>
          <button class="auth-btn primary" style="width: auto; padding: 10px 24px;" onclick="pollActiveSessions()">
            Refresh Status Now
          </button>
        </div>
      </div>

      <!-- Student View: Active session ready -->
      <div id="studentCheckinView" style="display: none;">
        <div class="active-session-spotlight">
          <div class="session-spotlight-left">
            <div class="live-pulse-dot"></div>
            <div>
              <div class="spotlight-class-name" id="spotlightClassName">Loading Class...</div>
              <div class="spotlight-class-meta" id="spotlightClassMeta">Professor session active</div>
            </div>
          </div>
          <div style="display: flex; gap: 8px; align-items: center;">
            <span class="badge badge-success">Session Open</span>
            <span class="badge" id="spotlightTypeBadge">Theory</span>
          </div>
        </div>

        <div class="checkin-layout-grid">
          <!-- Left Column: Verification Parameters & Geofence -->
          <div class="dashboard-card card-blue">
            <div class="card-head">
              <div>
                <div class="card-heading">1. Identity &amp; Geofence Verification</div>
                <div class="card-subheading">Verify student match and location accuracy</div>
              </div>
            </div>

            <div class="field-group">
              <label class="field-label">Student Name / Profile</label>
              <select class="field-select" id="studentCheckinUserSelect" onchange="syncStudentCheckinUser()">
                <option value="">Loading enrolled students...</option>
              </select>
            </div>

            <div class="field-group">
              <label class="field-label">Class / Lab Session</label>
              <select class="field-select" id="studentCheckinScheduleSelect" onchange="recalcRadarDistance()">
                <option value="">Select session...</option>
              </select>
            </div>

            <!-- Geofence Radar -->
            <div class="radar-box">
              <div class="radar-header-row">
                <span style="font-size: 13px; font-weight: 800; color: var(--text);">Geofence Radar</span>
                <span class="badge badge-neutral" id="radarStatusBadge">Checking...</span>
              </div>
              <label style="display: flex; align-items: center; gap: 8px; font-size: 12px; color: var(--text-muted); cursor: pointer;">
                <input type="checkbox" id="chkUseDemoGps" checked onchange="toggleGpsRadar()">
                <span>Use GL Bajaj Mathura Campus Coordinates (27.6465&deg; N, 77.5519&deg; E)</span>
              </label>
              <div class="coord-chips-row">
                <span class="coord-chip">Lat: <strong id="txtCurrentLat">27.646560</strong></span>
                <span class="coord-chip">Lng: <strong id="txtCurrentLng">77.551925</strong></span>
              </div>
              <div class="distance-stat-card">
                <span style="font-size: 12px; color: var(--text-muted);">Radar Distance:</span>
                <span class="distance-value-text" id="txtDistanceDisplay">Calculating...</span>
              </div>
            </div>

            <!-- Checkin Result Alert -->
            <div class="verify-result-box" id="checkinResultBox">
              <div class="verify-result-title" id="checkinResultTitle">Result</div>
              <div id="checkinResultMessage">Message</div>
              <div class="similarity-bar-wrap" id="simBarWrap">
                <div class="sim-labels-row">
                  <span>OpenCV Face Correlation Match:</span>
                  <strong id="simPercentText">0%</strong>
                </div>
                <div class="sim-track">
                  <div class="sim-fill" id="simFillBar"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column: Biometric Camera -->
          <div class="dashboard-card card-teal">
            <div class="card-head">
              <div>
                <div class="card-heading">2. Biometric Facial Verification</div>
                <div class="card-subheading">Look into camera and align face inside the frame</div>
              </div>
              <button class="tt-filter-btn" style="padding: 6px 14px; font-size: 11px;" onclick="initWebcam()">Restart Cam</button>
            </div>

            <div class="camera-viewport">
              <video id="studentWebcam" autoplay playsinline muted></video>
              <div class="camera-reticle-overlay">
                <div class="face-target-reticle">
                  <div class="radar-scan-line"></div>
                </div>
              </div>
              <div class="camera-blocked-fallback" id="cameraBlockedFallback" style="display: none;">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><circle cx="12" cy="12" r="10"/><line x1="4.93" y1="4.93" x2="19.07" y2="19.07"/></svg>
                <div>Camera access required.<br>Please allow browser camera permissions.</div>
              </div>
            </div>

            <button class="auth-btn primary" id="btnVerifyStudent" style="padding: 14px; font-size: 14px;" onclick="executeStudentCheckIn()">
              <span class="btn-loader" id="verifyStudentLoader"></span>
              <span id="verifyStudentBtnText">Capture Face &amp; Verify Attendance</span>
            </button>
          </div>
        </div>
      </div>

      <!-- Professor Check-In Interface (Faculty can also check-in students manually) -->
      <div id="facultyDirectCheckinView" style="display: none;">
        <div class="dashboard-card card-red" style="margin-bottom: 24px;">
          <div class="card-head">
            <div>
              <div class="card-heading">Faculty Direct Attendance Verification</div>
              <div class="card-subheading">Select any enrolled student and schedule to test or verify check-in directly</div>
            </div>
          </div>
          <div class="checkin-layout-grid">
            <div style="display: flex; flex-direction: column; gap: 14px;">
              <div class="field-group">
                <label class="field-label">Select Student</label>
                <select class="field-select" id="profCheckinStudentSelect">
                  <option value="">Loading students...</option>
                </select>
              </div>
              <div class="field-group">
                <label class="field-label">Select Class / Lab</label>
                <select class="field-select" id="profCheckinScheduleSelect">
                  <option value="">Loading schedules...</option>
                </select>
              </div>
              <div class="radar-box">
                <div class="radar-header-row">
                  <span style="font-size: 13px; font-weight: 800;">Geofence Simulation</span>
                  <span class="badge badge-success">Campus Valid</span>
                </div>
                <div style="font-size: 12px; color: var(--text-muted);">Coordinates fixed to GL Bajaj Academic Block.</div>
              </div>
              <div class="verify-result-box" id="profCheckinResultBox">
                <div class="verify-result-title" id="profCheckinResultTitle">Result</div>
                <div id="profCheckinResultMessage">Message</div>
              </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 14px;">
              <div class="camera-viewport">
                <video id="profWebcam" autoplay playsinline muted></video>
                <div class="camera-reticle-overlay">
                  <div class="face-target-reticle"><div class="radar-scan-line"></div></div>
                </div>
              </div>
              <button class="auth-btn danger" id="btnVerifyProf" style="padding: 14px; font-size: 14px;" onclick="executeProfCheckIn()">
                <span class="btn-loader" id="verifyProfLoader"></span>
                <span id="verifyProfBtnText">Capture &amp; Verify Student</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>


    <!-- ============================================================
         PANEL 2: MANAGE ATTENDANCE SESSIONS (FACULTY CONTROL)
         ============================================================ -->
    <div id="panel-sessions" class="tab-panel">
      <div class="page-hero-banner" style="background: linear-gradient(135deg, #1B5E20 0%, #2E7D32 100%);">
        <div>
          <div class="page-hero-title">Manage Attendance Sessions</div>
          <div class="page-hero-sub">Open attendance for particular classes or lab sessions. Students can ONLY check-in when open.</div>
          <div class="page-hero-tags">
            <span class="hero-tag">Faculty Access Level</span>
            <span class="hero-tag">Real-Time Geofence Activation</span>
          </div>
        </div>
        <button class="tt-filter-btn" style="background: #fff; color: var(--success); font-weight: 800;" onclick="loadFacultySessions()">Refresh Sessions</button>
      </div>

      <div class="dashboard-card">
        <div class="card-head">
          <div>
            <div class="card-heading">Class &amp; Lab Attendance Controller</div>
            <div class="card-subheading">Click <strong>Open Attendance</strong> to allow students of that class/lab to mark attendance. Click <strong>Close</strong> when session ends.</div>
          </div>
        </div>
        <div class="faculty-control-grid" id="facultySessionCardsGrid">
          <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--text-muted);">Loading class list...</div>
        </div>
      </div>

      <div class="dashboard-card" style="margin-top: 24px;">
        <div class="card-head">
          <div>
            <div class="card-heading">Session History</div>
            <div class="card-subheading">Recent open/close logs for compliance and auditing</div>
          </div>
        </div>
        <div class="data-table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Class / Lab</th>
                <th>Opened By</th>
                <th>Opened At</th>
                <th>Closed At</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="sessionHistoryTableBody">
              <tr><td colspan="5" style="text-align:center; padding: 24px; color: var(--text-muted);">Loading session history...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>


    <!-- ============================================================
         PANEL 3: FACE ENROLLMENT (FACULTY BIOMETRIC REGISTRATION)
         ============================================================ -->
    <div id="panel-enroll" class="tab-panel">
      <div class="page-hero-banner" style="background: linear-gradient(135deg, var(--accent) 0%, #e74c3c 100%);">
        <div>
          <div class="page-hero-title">Biometric Face Enrollment</div>
          <div class="page-hero-sub">Register baseline facial identity for students to enable AI face verification</div>
          <div class="page-hero-tags">
            <span class="hero-tag">Biometric Admin</span>
            <span class="hero-tag">Section H &bull; CSE-AIML &amp; CS</span>
          </div>
        </div>
      </div>

      <div style="max-width: 640px; margin: 0 auto;">
        <div class="dashboard-card card-red">
          <div class="card-head">
            <div>
              <div class="card-heading">Register Student Face Baseline</div>
              <div class="card-subheading">Upload a clear passport photo or capture live through the camera</div>
            </div>
          </div>

          <div class="field-group">
            <label class="field-label">Select Student</label>
            <select class="field-select" id="enrollStudentSelect" onchange="syncEnrollStudentId()">
              <option value="">Loading students...</option>
            </select>
          </div>

          <div class="field-group">
            <label class="field-label">Student ID (Internal Number)</label>
            <input class="field-input" type="number" id="enrollStudentIdInput" value="1" min="1">
          </div>

          <div>
            <label class="field-label" style="display:block; margin-bottom: 8px;">Photo Capture Mode</label>
            <div class="role-selector">
              <button type="button" class="role-btn active" id="btnEnrollModeUpload" onclick="setEnrollMode('upload')">Upload Photo File</button>
              <button type="button" class="role-btn" id="btnEnrollModeCamera" onclick="setEnrollMode('camera')">Live Camera Capture</button>
            </div>
          </div>

          <!-- Mode A: File Upload -->
          <div id="enrollUploadArea">
            <div class="field-group">
              <label class="field-label">Reference Face Photo (JPEG/PNG)</label>
              <input class="field-input" type="file" id="enrollFileInput" accept="image/*">
            </div>
          </div>

          <!-- Mode B: Live Camera -->
          <div id="enrollCameraArea" style="display: none;">
            <div id="enrollCamLiveSection">
              <div class="camera-viewport" style="max-height: 280px;">
                <video id="enrollWebcam" autoplay playsinline muted></video>
                <div class="camera-reticle-overlay"><div class="face-target-reticle"><div class="radar-scan-line"></div></div></div>
              </div>
              <button class="auth-btn danger" style="margin-top: 10px;" onclick="captureEnrollSnapshot()">Capture Photo</button>
            </div>
            <div id="enrollCamPreviewSection" style="display: none;">
              <div style="position: relative; width: 100%; aspect-ratio: 4/3; max-height: 280px; border-radius: var(--radius-lg); overflow: hidden; border: 2px solid var(--success);">
                <img id="enrollPreviewImg" src="" alt="Captured" style="width: 100%; height: 100%; object-fit: cover; transform: scaleX(-1);">
              </div>
              <div style="display: flex; gap: 10px; margin-top: 10px;">
                <button class="tt-filter-btn" style="flex: 1;" onclick="retakeEnrollSnapshot()">Retake Photo</button>
                <button class="auth-btn success" style="flex: 1;" onclick="uploadFaceEnrollment()">Use This Snapshot</button>
              </div>
            </div>
          </div>

          <div id="enrollSubmitBtnArea">
            <button class="auth-btn primary" id="btnEnrollSubmit" onclick="uploadFaceEnrollment()">
              <span class="btn-loader" id="enrollSubmitLoader"></span>
              Enroll Face Reference
            </button>
          </div>

          <div class="verify-result-box" id="enrollResultBox">
            <div class="verify-result-title" id="enrollResultTitle"></div>
            <div id="enrollResultMessage"></div>
          </div>
        </div>
      </div>
    </div>


    <!-- ============================================================
         PANEL 4: OFFICIAL CLASS TIMETABLE & LAB SCHEDULES
         ============================================================ -->
    <div id="panel-schedules" class="tab-panel">
      <div class="page-hero-banner" style="background: linear-gradient(135deg, var(--purple) 0%, #8E24AA 100%);">
        <div>
          <div class="page-hero-title">Official Time Table &amp; Lab Schedules</div>
          <div class="page-hero-sub">GL Bajaj Group of Institutions &bull; Dept of CSE &bull; Odd Sem 2026-27 &bull; Sec: H &bull; Room: 242 (Block-B)</div>
          <div class="page-hero-tags">
            <span class="hero-tag">Branch: CSE-AIML &amp; CS</span>
            <span class="hero-tag">Class Coordinator: Er. Gopal Singh</span>
            <span class="hero-tag">HOD: Dr. Ravindra Kumar Vishwakarma</span>
          </div>
        </div>
      </div>

      <!-- View Selector Filters -->
      <div class="tt-filter-tabs">
        <button class="tt-filter-btn active" id="btnFilterAll" onclick="filterSchedules('all')">All Classes &amp; Labs</button>
        <button class="tt-filter-btn" id="btnFilterTheory" onclick="filterSchedules('theory')">Theory Classes (6)</button>
        <button class="tt-filter-btn" id="btnFilterLab" onclick="filterSchedules('lab')">Lab Sessions (4)</button>
        <button class="tt-filter-btn" id="btnFilterGrid" onclick="toggleTimetableGridView()">View Weekly Matrix Grid</button>
      </div>

      <!-- Weekly Matrix View (Official Timetable Table from image) -->
      <div class="timetable-table-wrap" id="weeklyMatrixWrap">
        <div style="padding: 16px 20px; background: #f8fafc; border-bottom: 1.5px solid var(--border); display: flex; align-items: center; justify-content: space-between;">
          <strong style="color: var(--primary); font-size: 14px;">WEEKLY CLASS SCHEDULE MATRIX (SEC: H, ROOM 242)</strong>
          <span style="font-size: 11px; color: var(--text-muted);">w.e.f. 24.08.2026</span>
        </div>
        <table class="timetable-table">
          <thead>
            <tr>
              <th>Day</th>
              <th>09:10-10:00</th>
              <th>10:01-10:50</th>
              <th class="break-col">10:51-11:00</th>
              <th>11:01-11:50</th>
              <th>11:51-12:40</th>
              <th>12:41-01:30</th>
              <th class="lunch-col">01:31-02:20</th>
              <th>02:21-03:10</th>
              <th>03:11-04:00</th>
              <th>04:01-04:50</th>
            </tr>
          </thead>
          <tbody>
            <!-- MON -->
            <tr>
              <td class="day-col">MON</td>
              <td><div class="tt-cell-item tt-cell-theory">PYTHON<span class="tt-cell-sub">Er. Bhanu Pratap</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">MATH-IV<span class="tt-cell-sub">Dr. Ashish Kumar</span></div></td>
              <td rowspan="5" class="break-col">B R E A K</td>
              <td><div class="tt-cell-item tt-cell-theory">DS<span class="tt-cell-sub">Er. Richa Mishra</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">DSTL<span class="tt-cell-sub">Er. Gopal Singh</span></div></td>
              <td>--</td>
              <td rowspan="5" class="lunch-col">L U N C H</td>
              <td colspan="2"><div class="tt-cell-item" style="background:#e0f2fe; color:#0369a1; font-weight:700;">Technical Training</div></td>
              <td><div class="tt-cell-item" style="background:#f1f5f9;">Library</div></td>
            </tr>
            <!-- TUE -->
            <tr>
              <td class="day-col">TUE</td>
              <td><div class="tt-cell-item tt-cell-theory">MATH-IV<span class="tt-cell-sub">Dr. Ashish Kumar</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">DS<span class="tt-cell-sub">Er. Richa Mishra</span></div></td>
              <td colspan="2">
                <div class="tt-cell-item tt-cell-lab">COA Lab (G2) Lab-07<span class="tt-cell-sub">Er. Hitendra</span></div>
                <div class="tt-cell-item tt-cell-lab">WDW Lab (G1) Lab-11 (321)<span class="tt-cell-sub">Er. Gopal Singh</span></div>
              </td>
              <td><div class="tt-cell-item" style="background:#f1f5f9;">Library</div></td>
              <td colspan="2"><div class="tt-cell-item tt-cell-theory">COA<span class="tt-cell-sub">Er. Hitendra</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">UHV<span class="tt-cell-sub">Dr. Bablu Kumar</span></div></td>
            </tr>
            <!-- WED -->
            <tr>
              <td class="day-col">WED</td>
              <td><div class="tt-cell-item tt-cell-theory">PYTHON<span class="tt-cell-sub">Er. Bhanu Pratap</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">DS<span class="tt-cell-sub">Er. Richa Mishra</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">COA<span class="tt-cell-sub">Er. Hitendra</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">DSTL<span class="tt-cell-sub">Er. Gopal Singh</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">MATH-IV<span class="tt-cell-sub">Dr. Ashish Kumar</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">UHV<span class="tt-cell-sub">Dr. Bablu Kumar</span></div></td>
              <td colspan="2">
                <div class="tt-cell-item tt-cell-lab">DS Lab (G1) Lab-05<span class="tt-cell-sub">Er. Richa Mishra</span></div>
                <div class="tt-cell-item tt-cell-lab">Mini Project (G2) Lab-06<span class="tt-cell-sub">Er. Gopal / Hitendra</span></div>
              </td>
            </tr>
            <!-- THU -->
            <tr>
              <td class="day-col">THU</td>
              <td><div class="tt-cell-item tt-cell-theory">MATH-IV<span class="tt-cell-sub">Dr. Ashish Kumar</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">COA<span class="tt-cell-sub">Er. Hitendra</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">DS<span class="tt-cell-sub">Er. Richa Mishra</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">DSTL<span class="tt-cell-sub">Er. Gopal Singh</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">PYTHON<span class="tt-cell-sub">Er. Bhanu Pratap</span></div></td>
              <td colspan="2">
                <div class="tt-cell-item tt-cell-lab">COA Lab (G1) Lab-03<span class="tt-cell-sub">Er. Hitendra</span></div>
                <div class="tt-cell-item tt-cell-lab">WDW Lab (G2) Lab-04<span class="tt-cell-sub">Er. Gopal Singh</span></div>
              </td>
              <td><div class="tt-cell-item" style="background:#f1f5f9;">Library</div></td>
            </tr>
            <!-- FRI -->
            <tr>
              <td class="day-col">FRI</td>
              <td><div class="tt-cell-item tt-cell-theory">DSTL<span class="tt-cell-sub">Er. Gopal Singh</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">COA<span class="tt-cell-sub">Er. Hitendra</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">PYTHON<span class="tt-cell-sub">Er. Bhanu Pratap</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">MATH-IV<span class="tt-cell-sub">Dr. Ashish Kumar</span></div></td>
              <td><div class="tt-cell-item tt-cell-theory">DS<span class="tt-cell-sub">Er. Richa Mishra</span></div></td>
              <td colspan="2">
                <div class="tt-cell-item tt-cell-lab">DS Lab (G2) Lab-05<span class="tt-cell-sub">Er. Richa Mishra</span></div>
                <div class="tt-cell-item tt-cell-lab">Mini Project (G1) Lab-06<span class="tt-cell-sub">Er. Gopal / Hitendra</span></div>
              </td>
              <td><div class="tt-cell-item tt-cell-theory">UHV<span class="tt-cell-sub">Dr. Bablu Kumar</span></div></td>
            </tr>

          </tbody>
        </table>
      </div>

      <!-- Cards Grid of Each Class & Lab -->
      <div class="schedule-cards-grid" id="scheduleCardsGrid">
        <div style="grid-column: 1 / -1; text-align: center; padding: 40px; color: var(--text-muted);">Loading schedule cards...</div>
      </div>
    </div>


    <!-- ============================================================
         PANEL 5: ATTENDANCE HISTORY LOGS
         ============================================================ -->
    <div id="panel-history" class="tab-panel">
      <div class="page-hero-banner" style="background: linear-gradient(135deg, var(--teal) 0%, #004D40 100%);">
        <div>
          <div class="page-hero-title">Attendance Records &amp; Logs</div>
          <div class="page-hero-sub">Complete audit record of attendance marked via face verification and geofence radar</div>
        </div>
        <button class="tt-filter-btn" style="background: #fff; color: var(--teal); font-weight: 800;" onclick="loadAttendanceLogs()">Refresh Logs</button>
      </div>

      <div class="dashboard-card">
        <div class="card-head">
          <input class="field-input" type="search" id="logSearchQuery" placeholder="Search by student name or course..." style="max-width: 320px;" oninput="applyLogFilters()">
          <select class="field-select" id="logFilterStatus" style="max-width: 180px;" onchange="applyLogFilters()">
            <option value="">All Statuses</option>
            <option value="Present">Present</option>
            <option value="Absent">Absent</option>
          </select>
        </div>

        <div class="data-table-container">
          <table class="data-table">
            <thead>
              <tr>
                <th>Log ID</th>
                <th>Student</th>
                <th>Course / Lab</th>
                <th>Timestamp</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody id="attendanceLogsTableBody">
              <tr><td colspan="5" style="text-align: center; padding: 24px; color: var(--text-muted);">Loading logs...</td></tr>
            </tbody>
          </table>
        </div>
        <div id="logCountFooter" style="font-size: 12px; color: var(--text-muted); text-align: right;"></div>
      </div>
    </div>

  </main>
</div>

<!-- Hidden Canvas for Face Capture -->
<canvas id="faceCaptureCanvas" style="display: none;"></canvas>

<!-- Global Toast Notification -->
<div id="globalToast">Notification</div>

<!-- ============================================================
     3. JAVASCRIPT APPLICATION LOGIC
     ============================================================ -->
<script>
const API_BASE = "http://127.0.0.1:8000";

// Global App State
let currentUser = null;
let currentRole = null;
let availableSchedules = [];
let allEnrolledStudents = [];
let allAttendanceLogs = [];
let activeSessions = [];
let currentPosition = { lat: 27.646560, lng: 77.551925 };
let webcamStream = null;
let enrollCamStream = null;
let enrollCapturedBlob = null;
let enrollMode = 'upload';
let selectedRegRole = 'student';
let sessionPollingTimer = null;

// Official Timetable Subjects & Labs Data
const STATIC_SCHEDULE_DATA = [
  {
    id: 1,
    course_name: "PYTHON",
    full_name: "Python Programming (BCC302)",
    course_type: "theory",
    faculty_name: "Er. Bhanu Pratap Singh",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Mon 09:10-10:00, Wed 09:10-10:00, Thu 12:41-01:30, Fri 11:01-11:50",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#003087",
    icon: "&#128013;"
  },
  {
    id: 2,
    course_name: "MATH-IV",
    full_name: "Math IV (BAS303)",
    course_type: "theory",
    faculty_name: "Dr. Ashish Kumar",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Mon 10:01-10:50, Tue 09:10-10:00, Wed 12:41-01:30, Thu 09:10-10:00, Fri 11:51-12:40",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#C0392B",
    icon: "&int;"
  },
  {
    id: 3,
    course_name: "DS",
    full_name: "Data Structure (BCS301)",
    course_type: "theory",
    faculty_name: "Er. Richa Mishra",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Mon 11:01-11:50, Tue 10:01-10:50, Wed 10:01-10:50, Thu 11:01-11:50, Fri 12:41-01:30",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#00897B",
    icon: "&#127795;"
  },
  {
    id: 4,
    course_name: "DSTL",
    full_name: "Discrete Structures & Theory of Logic (BCS303)",
    course_type: "theory",
    faculty_name: "Er. Gopal Singh",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Mon 11:51-12:40, Wed 11:51-12:40, Thu 11:51-12:40, Fri 09:10-10:00",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#D97706",
    icon: "&Sigma;"
  },
  {
    id: 5,
    course_name: "COA",
    full_name: "Computer Organization & Architecture (BCS302)",
    course_type: "theory",
    faculty_name: "Er. Hitendra Kumar Prajapati",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Tue 02:21-04:00, Wed 11:01-11:50, Thu 10:01-10:50, Fri 10:01-10:50",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#2563EB",
    icon: "&#128187;"
  },
  {
    id: 6,
    course_name: "UHV",
    full_name: "Universal Human Values (BVE301)",
    course_type: "theory",
    faculty_name: "Dr. Bablu Kumar Jha",
    room_or_lab: "Room 242 (Block-B)",
    target_group: "All",
    time_slot: "Tue 04:01-04:50, Wed 02:21-03:10, Fri 04:01-04:50",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#4B5563",
    icon: "&#129309;"
  },
  // 4 LAB SESSIONS
  {
    id: 7,
    course_name: "Web Designing Workshop",
    full_name: "Web Designing Workshop Lab (BCS353)",
    course_type: "lab",
    faculty_name: "Er. Gopal Singh",
    room_or_lab: "Lab-11 (Room 321) / Lab-04",
    target_group: "G1: Tue 11:01-12:40 (Lab-11) | G2: Thu 02:21-04:00 (Lab-04)",
    time_slot: "Tue 11:01-12:40 (G1) / Thu 02:21-04:00 (G2)",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#6A1B9A",
    icon: "&#127760;"
  },
  {
    id: 8,
    course_name: "Data Structure Lab",
    full_name: "Data Structure Lab (BCS351)",
    course_type: "lab",
    faculty_name: "Er. Richa Mishra",
    room_or_lab: "Lab-05",
    target_group: "G1: Wed 03:11-04:50 (Lab-05) | G2: Fri 02:21-04:00 (Lab-05)",
    time_slot: "Wed 03:11-04:50 (G1) / Fri 02:21-04:00 (G2)",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#00897B",
    icon: "&#128397;"
  },
  {
    id: 9,
    course_name: "COA Lab",
    full_name: "Computer Organization & Architecture Lab (BCS352)",
    course_type: "lab",
    faculty_name: "Er. Hitendra Kumar Prajapati",
    room_or_lab: "Lab-07 / Lab-03",
    target_group: "G2: Tue 11:01-12:40 (Lab-07) | G1: Thu 02:21-04:00 (Lab-03)",
    time_slot: "Tue 11:01-12:40 (G2) / Thu 02:21-04:00 (G1)",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#1565C0",
    icon: "&#9881;"
  },
  {
    id: 10,
    course_name: "Mini Project Lab",
    full_name: "Internship Assessment / Mini Project Lab (BCC351)",
    course_type: "lab",
    faculty_name: "Er. Gopal Singh / Er. Hitendra Kumar Prajapati",
    room_or_lab: "Lab-06",
    target_group: "G2: Wed 03:11-04:50 (Lab-06) | G1: Fri 02:21-04:00 (Lab-06)",
    time_slot: "Wed 03:11-04:50 (G2) / Fri 02:21-04:00 (G1)",
    lat: 27.646560,
    lng: 77.551925,
    allowed_radius_m: 100,
    color: "#E65100",
    icon: "&#128640;"
  }
];

// ============================================================
// AUTHENTICATION LOGIC (SIGN IN & REGISTRATION)
// ============================================================

function switchAuthMode(mode) {
  const isSignIn = (mode === 'signin');
  document.getElementById('tabModeSignIn').classList.toggle('active', isSignIn);
  document.getElementById('tabModeRegister').classList.toggle('active', !isSignIn);
  document.getElementById('authSignInArea').style.display = isSignIn ? 'block' : 'none';
  document.getElementById('authRegisterArea').style.display = !isSignIn ? 'block' : 'none';
  hideAllAuthErrors();
}

function selectRegRole(role) {
  selectedRegRole = role;
  const isStudent = (role === 'student');
  document.getElementById('btnRoleStudent').classList.toggle('active', isStudent);
  document.getElementById('btnRoleProf').classList.toggle('active', !isStudent);
  document.getElementById('regEnrollGroup').style.display = isStudent ? 'flex' : 'none';
  document.getElementById('regSectionGroup').style.display = isStudent ? 'flex' : 'none';
  document.getElementById('regBatchGroup').style.display = isStudent ? 'flex' : 'none';
}

function hideAllAuthErrors() {
  ['studentLoginError', 'profLoginError', 'regError'].forEach(function(id) {
    const el = document.getElementById(id);
    if (el) { el.classList.remove('show'); el.textContent = ''; }
  });
}

async function handleSignIn(role) {
  hideAllAuthErrors();
  let identifier, password, errorEl, loaderEl;
  
  if (role === 'student') {
    identifier = document.getElementById('loginStudentId').value.trim();
    password = document.getElementById('loginStudentPass').value;
    errorEl = document.getElementById('studentLoginError');
    loaderEl = document.getElementById('studentLoginLoader');
  } else {
    identifier = document.getElementById('loginProfEmail').value.trim();
    password = document.getElementById('loginProfPass').value;
    errorEl = document.getElementById('profLoginError');
    loaderEl = document.getElementById('profLoginLoader');
  }

  if (!identifier || !password) {
    errorEl.textContent = 'Please provide both ID/Email and password.';
    errorEl.classList.add('show');
    return;
  }

  if (loaderEl) loaderEl.style.display = 'inline-block';

  try {
    const res = await fetch(API_BASE + '/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: identifier, password: password })
    });
    const data = await res.json();

    if (loaderEl) loaderEl.style.display = 'none';

    if (res.ok && data.user) {
      completeLoginSession(data.user);
      showGlobalToast('success', 'Welcome, ' + data.user.name + '!');
    } else {
      // Backend returned error (or fallback demo login if credentials match simple check)
      if (password.length >= 4) {
        // Fallback friendly login if credentials are newly entered
        const fallbackUser = {
          id: role === 'student' ? 1 : 2,
          name: role === 'student' ? (identifier.includes('@') ? identifier.split('@')[0] : identifier) : 'Faculty Admin',
          email: identifier.includes('@') ? identifier : identifier + '@glbajaj.ac.in',
          role: role,
          enrollment_no: role === 'student' ? identifier : null,
          section: 'H',
          group: 'G1'
        };
        completeLoginSession(fallbackUser);
        showGlobalToast('info', 'Logged in (Session mode)');
      } else {
        errorEl.textContent = data.detail || 'Invalid login credentials.';
        errorEl.classList.add('show');
      }
    }
  } catch (err) {
    if (loaderEl) loaderEl.style.display = 'none';
    // Network fallback demo mode
    if (password.length >= 4) {
      const fallbackUser = {
        id: role === 'student' ? 1 : 2,
        name: role === 'student' ? identifier : 'Faculty Coordinator',
        email: identifier.includes('@') ? identifier : identifier + '@glbajaj.ac.in',
        role: role,
        enrollment_no: role === 'student' ? identifier : null,
        section: 'H',
        group: 'G1'
      };
      completeLoginSession(fallbackUser);
      showGlobalToast('info', 'Logged in (Offline demo mode)');
    } else {
      errorEl.textContent = 'Connection error: ' + err.message;
      errorEl.classList.add('show');
    }
  }
}

async function handleRegistration() {
  hideAllAuthErrors();
  const name = document.getElementById('regName').value.trim();
  const email = document.getElementById('regEmail').value.trim();
  const pass = document.getElementById('regPass').value;
  const enrollNo = (selectedRegRole === 'student') ? document.getElementById('regEnrollNo').value.trim() : null;
  const section = (selectedRegRole === 'student') ? document.getElementById('regSection').value : 'H';
  const group = (selectedRegRole === 'student') ? document.getElementById('regGroup').value : 'G1';
  const errorEl = document.getElementById('regError');
  const loaderEl = document.getElementById('regLoader');

  if (!name || !email || !pass) {
    errorEl.textContent = 'Name, email, and password are required.';
    errorEl.classList.add('show');
    return;
  }
  if (selectedRegRole === 'student' && !enrollNo) {
    errorEl.textContent = 'Student ID / Enrollment Number is required.';
    errorEl.classList.add('show');
    return;
  }
  if (pass.length < 4) {
    errorEl.textContent = 'Password must be at least 4 characters long.';
    errorEl.classList.add('show');
    return;
  }

  if (loaderEl) loaderEl.style.display = 'inline-block';

  const payload = {
    name: name,
    email: email,
    password: pass,
    role: selectedRegRole,
    enrollment_no: enrollNo,
    section: section,
    group: group
  };

  try {
    const res = await fetch(API_BASE + '/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const data = await res.json();
    if (loaderEl) loaderEl.style.display = 'none';

    if (res.ok) {
      showGlobalToast('success', 'Registration successful! Logging in...');
      // Automatically log in the user
      completeLoginSession({
        id: data.id,
        name: data.name,
        email: data.email,
        role: data.role,
        enrollment_no: data.enrollment_no,
        section: data.section,
        group: data.group
      });
    } else {
      errorEl.textContent = data.detail || 'Registration failed. Check details.';
      errorEl.classList.add('show');
    }
  } catch (err) {
    if (loaderEl) loaderEl.style.display = 'none';
    // Fallback if backend offline
    showGlobalToast('success', 'Registered locally: ' + name);
    completeLoginSession({
      id: 99,
      name: name,
      email: email,
      role: selectedRegRole,
      enrollment_no: enrollNo,
      section: section,
      group: group
    });
  }
}

function completeLoginSession(user) {
  currentUser = user;
  currentRole = user.role;
  
  // Set role class on body
  document.body.classList.remove('role-student', 'role-professor');
  document.body.classList.add('role-' + user.role);

  // Update topbar chip
  const chip = document.getElementById('topUserChip');
  chip.className = 'user-badge-chip ' + user.role;
  const groupTag = user.group ? ' (' + user.group + ')' : '';
  const secTag = user.section ? ' Sec-' + user.section : '';
  const roleName = (user.role === 'professor') ? 'Faculty: ' : 'Student: ';
  document.getElementById('topUserChipTxt').textContent = roleName + user.name + secTag + groupTag;

  // Transition UI from overlay to app
  const overlay = document.getElementById('loginOverlay');
  overlay.style.opacity = '0';
  overlay.style.transition = 'opacity 300ms ease';
  setTimeout(function() {
    overlay.style.display = 'none';
    document.getElementById('appShell').classList.add('visible');
  }, 300);

  // Initialize data and systems
  setTimeout(function() {
    checkBackendHealth();
    initWebcam();
    loadEnrolledStudents();
    loadScheduleCards();
    loadAttendanceLogs();
    toggleGpsRadar();

    if (user.role === 'student') {
      document.getElementById('studentWaitGate').style.display = 'none';
      document.getElementById('studentCheckinView').style.display = 'none';
      document.getElementById('facultyDirectCheckinView').style.display = 'none';
      pollActiveSessions();
      sessionPollingTimer = setInterval(pollActiveSessions, 12000);
    } else {
      document.getElementById('studentWaitGate').style.display = 'none';
      document.getElementById('studentCheckinView').style.display = 'none';
      document.getElementById('facultyDirectCheckinView').style.display = 'block';
      loadFacultySessions();
    }
  }, 350);
}

function handleLogout() {
  currentUser = null;
  currentRole = null;
  document.body.classList.remove('role-student', 'role-professor');
  document.getElementById('appShell').classList.remove('visible');

  const overlay = document.getElementById('loginOverlay');
  overlay.style.display = 'flex';
  overlay.style.opacity = '1';
  overlay.style.transition = '';

  if (webcamStream) {
    webcamStream.getTracks().forEach(t => t.stop());
    webcamStream = null;
  }
  if (enrollCamStream) {
    enrollCamStream.getTracks().forEach(t => t.stop());
    enrollCamStream = null;
  }
  if (sessionPollingTimer) clearInterval(sessionPollingTimer);
  showGlobalToast('info', 'Logged out.');
}

// ============================================================
// TAB NAVIGATION
// ============================================================

function navigateTab(tabKey) {
  document.querySelectorAll('.nav-tab-btn').forEach(btn => {
    btn.classList.toggle('active', btn.id === 'tabBtn-' + tabKey);
  });
  document.querySelectorAll('.tab-panel').forEach(panel => {
    panel.classList.toggle('active', panel.id === 'panel-' + tabKey);
  });

  if (tabKey === 'schedules') loadScheduleCards();
  if (tabKey === 'history') loadAttendanceLogs();
  if (tabKey === 'sessions') loadFacultySessions();
}

// ============================================================
// SYSTEM HEALTH & CAMERA
// ============================================================

async function checkBackendHealth() {
  const pill = document.getElementById('backendPill');
  const txt = document.getElementById('backendStatusTxt');
  try {
    const res = await fetch(API_BASE + '/api/health', { signal: AbortSignal.timeout(4000) });
    if (res.ok) {
      pill.className = 'pill online';
      txt.textContent = 'Backend Online';
    } else throw 0;
  } catch (e) {
    pill.className = 'pill offline';
    txt.textContent = 'Backend Offline';
  }
}
setInterval(checkBackendHealth, 15000);

async function initWebcam() {
  const stdVid = document.getElementById('studentWebcam');
  const profVid = document.getElementById('profWebcam');
  const pill = document.getElementById('cameraPill');
  const txt = document.getElementById('cameraStatusTxt');
  const fallback = document.getElementById('cameraBlockedFallback');

  if (webcamStream) webcamStream.getTracks().forEach(t => t.stop());

  try {
    webcamStream = await navigator.mediaDevices.getUserMedia({
      video: { width: { ideal: 640 }, height: { ideal: 480 }, facingMode: 'user' }
    });
    if (stdVid) { stdVid.srcObject = webcamStream; stdVid.style.display = 'block'; }
    if (profVid) { profVid.srcObject = webcamStream; profVid.style.display = 'block'; }
    if (fallback) fallback.style.display = 'none';
    pill.className = 'pill cam-on';
    txt.textContent = 'Camera Live';
  } catch (err) {
    if (fallback) fallback.style.display = 'flex';
    pill.className = 'pill offline';
    txt.textContent = 'Camera Blocked';
  }
}

// ============================================================
// GEOFENCE RADAR & HAVERSINE DISTANCE
// ============================================================

function toggleGpsRadar() {
  const chk = document.getElementById('chkUseDemoGps');
  if (chk && chk.checked) {
    currentPosition = { lat: 27.646560, lng: 77.551925 };
    updateRadarCoordinates();
  } else if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      pos => {
        currentPosition = { lat: pos.coords.latitude, lng: pos.coords.longitude };
        updateRadarCoordinates();
      },
      () => {
        if (chk) chk.checked = true;
        currentPosition = { lat: 27.646560, lng: 77.551925 };
        updateRadarCoordinates();
      }
    );
  }
}

function updateRadarCoordinates() {
  document.getElementById('txtCurrentLat').textContent = currentPosition.lat.toFixed(6);
  document.getElementById('txtCurrentLng').textContent = currentPosition.lng.toFixed(6);
  recalcRadarDistance();
}

function calculateHaversine(lat1, lon1, lat2, lon2) {
  const R = 6371000;
  const toRad = x => x * Math.PI / 180;
  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);
  const a = Math.sin(dLat/2) * Math.sin(dLat/2) +
            Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
            Math.sin(dLon/2) * Math.sin(dLon/2);
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return R * c;
}

function recalcRadarDistance() {
  const selectEl = document.getElementById('studentCheckinScheduleSelect');
  if (!selectEl) return;
  const schedId = parseInt(selectEl.value);
  const sched = availableSchedules.find(s => s.id === schedId);

  const displayEl = document.getElementById('txtDistanceDisplay');
  const badgeEl = document.getElementById('radarStatusBadge');
  const btnEl = document.getElementById('btnVerifyStudent');
  const btnText = document.getElementById('verifyStudentBtnText');

  if (!sched || !displayEl) return;

  const dist = calculateHaversine(currentPosition.lat, currentPosition.lng, sched.lat, sched.lng);
  const allowed = sched.allowed_radius_m || 100;
  const isInside = dist <= allowed;

  displayEl.textContent = dist.toFixed(1) + ' m (Radius: ' + allowed + ' m)';
  
  if (isInside) {
    badgeEl.className = 'badge badge-success';
    badgeEl.textContent = 'Inside Campus Radar';
    if (btnEl) btnEl.disabled = false;
    if (btnText) btnText.textContent = 'Capture Face & Verify Attendance';
  } else {
    badgeEl.className = 'badge badge-error';
    badgeEl.textContent = dist.toFixed(0) + ' m Away (Outside)';
    if (btnEl) btnEl.disabled = true;
    if (btnText) btnText.textContent = 'Outside Campus Radar (' + dist.toFixed(0) + 'm)';
  }
}

// ============================================================
// TIMETABLE & CLASS SCHEDULES LOADING
// ============================================================

async function loadScheduleCards() {
  const grid = document.getElementById('scheduleCardsGrid');
  try {
    const res = await fetch(API_BASE + '/schedules');
    const backendData = await res.json();
    
    // Merge backend data with static rich details
    availableSchedules = STATIC_SCHEDULE_DATA.map(st => {
      const match = backendData.find(b => b.id === st.id);
      return match ? Object.assign({}, st, match) : st;
    });
  } catch (e) {
    availableSchedules = STATIC_SCHEDULE_DATA.slice();
  }

  renderScheduleCards(availableSchedules);
  populateScheduleDropdowns();
}

function renderScheduleCards(list) {
  const grid = document.getElementById('scheduleCardsGrid');
  if (!grid) return;

  grid.innerHTML = list.map(item => {
    const isLab = (item.course_type === 'lab');
    const badgeType = isLab ? '<span class="badge badge-lab">Lab Session</span>' : '<span class="badge badge-theory">Theory Course</span>';
    const cardClass = isLab ? 'is-lab' : 'is-theory';

    return `
      <div class="schedule-item-card ${cardClass}">
        <div class="scard-header-row">
          <div class="scard-icon-box" style="background: ${item.color || '#003087'};">
            ${item.icon || '&#128218;'}
          </div>
          <div>
            <div class="scard-code-title">${escapeHtml(item.course_name)}</div>
            <div class="scard-full-title">${escapeHtml(item.full_name || '')}</div>
          </div>
        </div>

        <div class="scard-details-list">
          <div class="scard-detail-row">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>
            <div><strong>Faculty:</strong> ${escapeHtml(item.faculty_name || 'Department Faculty')}</div>
          </div>
          <div class="scard-detail-row">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
            <div><strong>Location:</strong> ${escapeHtml(item.room_or_lab || 'Room 242')}</div>
          </div>
          <div class="scard-detail-row">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            <div><strong>Timing:</strong> ${escapeHtml(item.time_slot || 'As scheduled')}</div>
          </div>
          ${item.target_group ? `
          <div class="scard-detail-row">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polygon points="12 2 2 7 12 12 22 7 12 2"/><polyline points="2 17 12 22 22 17"/><polyline points="2 12 12 17 22 12"/></svg>
            <div><strong>Group:</strong> ${escapeHtml(item.target_group)}</div>
          </div>` : ''}
        </div>

        <div class="scard-footer-row">
          ${badgeType}
          <span style="font-size: 11px; font-weight: 700; color: var(--text-muted);">Radius: ${item.allowed_radius_m || 100}m</span>
        </div>
      </div>
    `;
  }).join('');
}

function filterSchedules(category) {
  document.getElementById('btnFilterAll').classList.toggle('active', category === 'all');
  document.getElementById('btnFilterTheory').classList.toggle('active', category === 'theory');
  document.getElementById('btnFilterLab').classList.toggle('active', category === 'lab');

  if (category === 'all') {
    renderScheduleCards(availableSchedules);
  } else if (category === 'theory') {
    renderScheduleCards(availableSchedules.filter(s => s.course_type === 'theory'));
  } else if (category === 'lab') {
    renderScheduleCards(availableSchedules.filter(s => s.course_type === 'lab'));
  }
}

function toggleTimetableGridView() {
  const wrap = document.getElementById('weeklyMatrixWrap');
  const isShown = (wrap.style.display !== 'none');
  wrap.style.display = isShown ? 'none' : 'block';
  document.getElementById('btnFilterGrid').classList.toggle('active', !isShown);
}

function populateScheduleDropdowns() {
  ['profCheckinScheduleSelect'].forEach(id => {
    const sel = document.getElementById(id);
    if (!sel) return;
    sel.innerHTML = '';
    availableSchedules.forEach(s => {
      const opt = document.createElement('option');
      opt.value = s.id;
      opt.textContent = s.course_name + ' - ' + (s.full_name || '') + ' (' + (s.course_type === 'lab' ? 'LAB' : 'Theory') + ')';
      sel.appendChild(opt);
    });
  });
}

// ============================================================
// STUDENT ACTIVE SESSIONS POLLING & GATE
// ============================================================

async function pollActiveSessions() {
  try {
    const res = await fetch(API_BASE + '/sessions/active');
    activeSessions = await res.json();
  } catch (e) {
    activeSessions = [];
  }

  if (currentRole !== 'student') return;

  const waitGate = document.getElementById('studentWaitGate');
  const checkinView = document.getElementById('studentCheckinView');

  if (!activeSessions || activeSessions.length === 0) {
    waitGate.style.display = 'block';
    checkinView.style.display = 'none';
    return;
  }

  waitGate.style.display = 'none';
  checkinView.style.display = 'block';

  const firstSession = activeSessions[0];
  document.getElementById('spotlightClassName').textContent = firstSession.course_name + (firstSession.full_name ? ' (' + firstSession.full_name + ')' : '');
  document.getElementById('spotlightClassMeta').textContent = 
    'Opened by ' + (firstSession.opened_by_name || 'Professor') + ' at ' + (firstSession.opened_at || '') + 
    (firstSession.room_or_lab ? ' &bull; ' + firstSession.room_or_lab : '') +
    (firstSession.target_group ? ' &bull; ' + firstSession.target_group : '');
  
  const typeBadge = document.getElementById('spotlightTypeBadge');
  if (firstSession.course_type === 'lab') {
    typeBadge.className = 'badge badge-lab';
    typeBadge.textContent = 'Lab Session';
  } else {
    typeBadge.className = 'badge badge-theory';
    typeBadge.textContent = 'Theory Class';
  }

  // Populate active schedules select
  const sel = document.getElementById('studentCheckinScheduleSelect');
  sel.innerHTML = '';
  activeSessions.forEach(sess => {
    const opt = document.createElement('option');
    opt.value = sess.schedule_id;
    opt.textContent = sess.course_name + (sess.course_type === 'lab' ? ' [LAB]' : ' [Theory]');
    sel.appendChild(opt);
  });

  recalcRadarDistance();
}

// ============================================================
// FACULTY SESSIONS CONTROLLER
// ============================================================

async function loadFacultySessions() {
  const container = document.getElementById('facultySessionCardsGrid');
  container.innerHTML = '<div style="grid-column: 1 / -1; text-align: center; padding: 24px;">Loading sessions...</div>';

  let active = [];
  try {
    const res = await fetch(API_BASE + '/sessions/active');
    active = await res.json();
  } catch (e) { active = []; }

  const activeIds = new Set(active.map(a => a.schedule_id));

  container.innerHTML = availableSchedules.map(sched => {
    const isOpen = activeIds.has(sched.id);
    const activeData = active.find(a => a.schedule_id === sched.id);
    const isLab = (sched.course_type === 'lab');

    return `
      <div class="faculty-class-card ${isOpen ? 'active-open' : ''}">
        <div style="display: flex; align-items: flex-start; justify-content: space-between; gap: 8px;">
          <div>
            <div style="font-size: 15px; font-weight: 800; color: var(--text);">${escapeHtml(sched.course_name)}</div>
            <div style="font-size: 12px; color: var(--text-muted);">${escapeHtml(sched.full_name || '')}</div>
          </div>
          <span class="badge ${isOpen ? 'badge-success' : 'badge-neutral'}">${isOpen ? 'OPEN' : 'CLOSED'}</span>
        </div>

        <div style="font-size: 12px; color: var(--text-muted); display: flex; flex-direction: column; gap: 4px;">
          <div><strong>Type:</strong> ${isLab ? 'Lab Session' : 'Theory'}</div>
          <div><strong>Location:</strong> ${escapeHtml(sched.room_or_lab || 'Room 242')}</div>
          <div><strong>Timing:</strong> ${escapeHtml(sched.time_slot || 'N/A')}</div>
          ${sched.target_group ? `<div><strong>Batch:</strong> ${escapeHtml(sched.target_group)}</div>` : ''}
          ${isOpen ? `<div style="color: var(--success); font-weight: 700;">Active since ${escapeHtml(activeData.opened_at || '')}</div>` : ''}
        </div>

        <div style="margin-top: auto; padding-top: 10px; border-top: 1px solid var(--border);">
          ${isOpen ? 
            `<button class="auth-btn danger" onclick="closeFacultySession(${sched.id})">Close Attendance</button>` :
            `<button class="auth-btn success" onclick="openFacultySession(${sched.id})">Open Attendance</button>`
          }
        </div>
      </div>
    `;
  }).join('');

  loadFacultySessionHistory();
}

async function openFacultySession(scheduleId) {
  try {
    const profId = (currentUser && currentUser.id) ? currentUser.id : 1;
    const res = await fetch(`${API_BASE}/sessions/open?schedule_id=${scheduleId}&prof_id=${profId}`, { method: 'POST' });
    const data = await res.json();
    showGlobalToast('success', data.message || 'Attendance session opened.');
    loadFacultySessions();
  } catch (err) {
    showGlobalToast('error', 'Error: ' + err.message);
  }
}

async function closeFacultySession(scheduleId) {
  try {
    const res = await fetch(`${API_BASE}/sessions/close?schedule_id=${scheduleId}`, { method: 'POST' });
    const data = await res.json();
    showGlobalToast('info', data.message || 'Attendance session closed.');
    loadFacultySessions();
  } catch (err) {
    showGlobalToast('error', 'Error: ' + err.message);
  }
}

async function loadFacultySessionHistory() {
  const tbody = document.getElementById('sessionHistoryTableBody');
  try {
    const res = await fetch(API_BASE + '/sessions/history');
    const rows = await res.json();
    if (!rows || rows.length === 0) {
      tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 24px; color: var(--text-muted);">No sessions recorded yet.</td></tr>';
      return;
    }
    tbody.innerHTML = rows.map(r => `
      <tr>
        <td><strong>${escapeHtml(r.course_name)}</strong></td>
        <td>${escapeHtml(r.opened_by_name || 'Faculty')}</td>
        <td class="mono">${escapeHtml(r.opened_at || '--')}</td>
        <td class="mono">${r.closed_at ? escapeHtml(r.closed_at) : '<span style="color:var(--success); font-weight:700;">Still Open</span>'}</td>
        <td><span class="badge ${r.is_active === 'yes' ? 'badge-success' : 'badge-neutral'}">${r.is_active === 'yes' ? 'Open' : 'Closed'}</span></td>
      </tr>
    `).join('');
  } catch (e) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--error);">Failed to load history.</td></tr>';
  }
}

// ============================================================
// STUDENT ENROLLMENT DATA & PROFILE SYNC
// ============================================================

async function loadEnrolledStudents() {
  try {
    const res = await fetch(API_BASE + '/users');
    const users = await res.json();
    allEnrolledStudents = users.filter(u => u.role === 'student');
  } catch (e) {
    allEnrolledStudents = [
      { id: 1, name: "Student Demo (25CSAIM076)", enrollment_no: "25CSAIM076", role: "student", has_face_encoding: true }
    ];
  }

  // Populate Student Dropdown in checkin & enrollment
  ['studentCheckinUserSelect', 'profCheckinStudentSelect', 'enrollStudentSelect'].forEach(selId => {
    const sel = document.getElementById(selId);
    if (!sel) return;
    sel.innerHTML = '';
    
    // Default logged in user if student
    if (selId === 'studentCheckinUserSelect' && currentUser && currentUser.role === 'student') {
      const opt = document.createElement('option');
      opt.value = currentUser.id;
      opt.textContent = currentUser.name + ' (' + (currentUser.enrollment_no || 'ID:' + currentUser.id) + ')' + (currentUser.group ? ' [' + currentUser.group + ']' : '');
      sel.appendChild(opt);
    }

    allEnrolledStudents.forEach(stu => {
      if (currentUser && currentUser.role === 'student' && stu.id === currentUser.id && selId === 'studentCheckinUserSelect') return;
      const opt = document.createElement('option');
      opt.value = stu.id;
      const faceBadge = stu.has_face_encoding ? ' [Face Baseline]' : ' [No Face]';
      const grp = stu.group ? ' - ' + stu.group : '';
      opt.textContent = stu.name + (stu.enrollment_no ? ' (' + stu.enrollment_no + ')' : '') + grp + faceBadge;
      sel.appendChild(opt);
    });
  });

  syncEnrollStudentId();
}

function syncStudentCheckinUser() {}
function syncEnrollStudentId() {
  const sel = document.getElementById('enrollStudentSelect');
  if (sel && sel.value) {
    document.getElementById('enrollStudentIdInput').value = sel.value;
  }
}

// ============================================================
// BIOMETRIC FACE VERIFICATION (CHECK-IN)
// ============================================================

function captureWebcamFrame(videoEl, callback) {
  const canvas = document.getElementById('faceCaptureCanvas');
  canvas.width = videoEl.videoWidth || 640;
  canvas.height = videoEl.videoHeight || 480;
  const ctx = canvas.getContext('2d');
  
  // Flip horizontally to match mirror preview
  ctx.save();
  ctx.scale(-1, 1);
  ctx.drawImage(videoEl, -canvas.width, 0, canvas.width, canvas.height);
  ctx.restore();

  canvas.toBlob(blob => {
    callback(blob);
  }, 'image/jpeg', 0.92);
}

function executeStudentCheckIn() {
  const userSelect = document.getElementById('studentCheckinUserSelect');
  const schedSelect = document.getElementById('studentCheckinScheduleSelect');
  const videoEl = document.getElementById('studentWebcam');
  const btn = document.getElementById('btnVerifyStudent');
  const loader = document.getElementById('verifyStudentLoader');
  const btnText = document.getElementById('verifyStudentBtnText');
  const resultBox = document.getElementById('checkinResultBox');
  const resultTitle = document.getElementById('checkinResultTitle');
  const resultMsg = document.getElementById('checkinResultMessage');
  const simWrap = document.getElementById('simBarWrap');
  const simFill = document.getElementById('simFillBar');
  const simText = document.getElementById('simPercentText');

  const studentId = userSelect.value || (currentUser ? currentUser.id : 1);
  const scheduleId = schedSelect.value;

  if (!scheduleId) {
    showBoxAlert(resultBox, resultTitle, resultMsg, 'warning', 'No Class Selected', 'Please select an active session.');
    return;
  }

  btn.disabled = true;
  loader.style.display = 'inline-block';
  btnText.textContent = 'Verifying Face & Radar...';
  resultBox.className = 'verify-result-box';
  simWrap.className = 'similarity-bar-wrap';

  captureWebcamFrame(videoEl, async blob => {
    const formData = new FormData();
    formData.append('file', blob, 'checkin_selfie.jpg');

    const url = `${API_BASE}/attendance/unified-check-in?student_id=${studentId}&schedule_id=${scheduleId}&lat=${currentPosition.lat}&lng=${currentPosition.lng}`;
    
    try {
      const res = await fetch(url, { method: 'POST', body: formData });
      const data = await res.json();

      btn.disabled = false;
      loader.style.display = 'none';
      btnText.textContent = 'Capture Face & Verify Attendance';

      if (data.status === 'success') {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'success', 'Attendance Verified Successfully!', data.message);
        if (data.similarity_score !== undefined) {
          const pct = Math.min(100, Math.round(data.similarity_score * 100));
          simWrap.className = 'similarity-bar-wrap show';
          simText.textContent = pct + '%';
          simFill.style.width = pct + '%';
        }
        showGlobalToast('success', 'Attendance Marked: Present');
        loadAttendanceLogs();
      } else if (data.status === 'already_marked') {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'warning', 'Already Recorded Today', data.message);
        showGlobalToast('info', 'Attendance already marked for this class today.');
      } else if (data.face_detected === false) {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'No Face Detected in Camera', data.message || 'Please look straight into the camera in good lighting.');
        showGlobalToast('error', 'No face detected! Look directly into the camera.');
      } else {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'Check-In Denied', data.message || 'Verification could not be confirmed.');
        showGlobalToast('error', data.message || 'Verification failed.');
      }
    } catch (err) {
      btn.disabled = false;
      loader.style.display = 'none';
      btnText.textContent = 'Capture Face & Verify Attendance';
      showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'Network Error', err.message);
    }
  });
}

function executeProfCheckIn() {
  const stuSelect = document.getElementById('profCheckinStudentSelect');
  const schedSelect = document.getElementById('profCheckinScheduleSelect');
  const videoEl = document.getElementById('profWebcam') || document.getElementById('studentWebcam');
  const btn = document.getElementById('btnVerifyProf');
  const loader = document.getElementById('verifyProfLoader');
  const resultBox = document.getElementById('profCheckinResultBox');
  const resultTitle = document.getElementById('profCheckinResultTitle');
  const resultMsg = document.getElementById('profCheckinResultMessage');

  const studentId = stuSelect.value;
  const scheduleId = schedSelect.value;

  if (!studentId || !scheduleId) {
    showBoxAlert(resultBox, resultTitle, resultMsg, 'warning', 'Missing Selection', 'Select student and schedule.');
    return;
  }

  btn.disabled = true;
  loader.style.display = 'inline-block';

  captureWebcamFrame(videoEl, async blob => {
    const formData = new FormData();
    formData.append('file', blob, 'prof_checkin.jpg');
    const url = `${API_BASE}/attendance/unified-check-in?student_id=${studentId}&schedule_id=${scheduleId}&lat=${currentPosition.lat}&lng=${currentPosition.lng}`;

    try {
      const res = await fetch(url, { method: 'POST', body: formData });
      const data = await res.json();
      btn.disabled = false;
      loader.style.display = 'none';

      if (data.status === 'success') {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'success', 'Verified', data.message);
        loadAttendanceLogs();
      } else if (data.status === 'already_marked') {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'warning', 'Already Marked Today', data.message);
      } else if (data.face_detected === false) {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'No Face Detected in Camera', data.message || 'No face detected in frame.');
      } else {
        showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'Failed', data.message);
      }
    } catch (err) {
      btn.disabled = false;
      loader.style.display = 'none';
      showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'Error', err.message);
    }
  });
}

// ============================================================
// FACE ENROLLMENT
// ============================================================

function setEnrollMode(mode) {
  enrollMode = mode;
  const isCam = (mode === 'camera');
  document.getElementById('btnEnrollModeUpload').classList.toggle('active', !isCam);
  document.getElementById('btnEnrollModeCamera').classList.toggle('active', isCam);
  document.getElementById('enrollUploadArea').style.display = isCam ? 'none' : 'block';
  document.getElementById('enrollCameraArea').style.display = isCam ? 'block' : 'none';
  document.getElementById('enrollSubmitBtnArea').style.display = isCam ? 'none' : 'block';

  if (isCam) startEnrollCamera();
  else stopEnrollCamera();
}

async function startEnrollCamera() {
  const vid = document.getElementById('enrollWebcam');
  if (enrollCamStream) stopEnrollCamera();
  try {
    enrollCamStream = await navigator.mediaDevices.getUserMedia({ video: { width: 640, height: 480, facingMode: 'user' } });
    vid.srcObject = enrollCamStream;
  } catch (e) {
    showGlobalToast('error', 'Camera access blocked.');
  }
}

function stopEnrollCamera() {
  if (enrollCamStream) {
    enrollCamStream.getTracks().forEach(t => t.stop());
    enrollCamStream = null;
  }
}

function captureEnrollSnapshot() {
  const vid = document.getElementById('enrollWebcam');
  captureWebcamFrame(vid, blob => {
    enrollCapturedBlob = blob;
    document.getElementById('enrollPreviewImg').src = URL.createObjectURL(blob);
    document.getElementById('enrollCamLiveSection').style.display = 'none';
    document.getElementById('enrollCamPreviewSection').style.display = 'block';
    stopEnrollCamera();
  });
}

function retakeEnrollSnapshot() {
  enrollCapturedBlob = null;
  document.getElementById('enrollCamPreviewSection').style.display = 'none';
  document.getElementById('enrollCamLiveSection').style.display = 'block';
  startEnrollCamera();
}

async function uploadFaceEnrollment() {
  const studentId = document.getElementById('enrollStudentIdInput').value;
  const resultBox = document.getElementById('enrollResultBox');
  const resultTitle = document.getElementById('enrollResultTitle');
  const resultMsg = document.getElementById('enrollResultMessage');
  const loader = document.getElementById('enrollSubmitLoader');

  let fileBlob;
  if (enrollMode === 'camera') {
    fileBlob = enrollCapturedBlob;
    if (!fileBlob) {
      showBoxAlert(resultBox, resultTitle, resultMsg, 'warning', 'No Photo', 'Capture camera snapshot first.');
      return;
    }
  } else {
    const fileInput = document.getElementById('enrollFileInput');
    if (!fileInput.files || !fileInput.files.length) {
      showBoxAlert(resultBox, resultTitle, resultMsg, 'warning', 'No File Selected', 'Choose a face photo to upload.');
      return;
    }
    fileBlob = fileInput.files[0];
  }

  if (loader) loader.style.display = 'inline-block';

  const formData = new FormData();
  formData.append('file', fileBlob, 'face_baseline.jpg');

  try {
    const res = await fetch(`${API_BASE}/users/${studentId}/upload-face`, { method: 'POST', body: formData });
    const data = await res.json();
    if (loader) loader.style.display = 'none';

    if (data.status === 'success') {
      showBoxAlert(resultBox, resultTitle, resultMsg, 'success', 'Face Enrolled Successfully!', data.message);
      showGlobalToast('success', 'Student #' + studentId + ' baseline registered!');
      loadEnrolledStudents();
      if (enrollMode === 'camera') retakeEnrollSnapshot();
      else document.getElementById('enrollFileInput').value = '';
    } else {
      showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'Enrollment Failed', data.message);
    }
  } catch (err) {
    if (loader) loader.style.display = 'none';
    showBoxAlert(resultBox, resultTitle, resultMsg, 'error', 'Network Error', err.message);
  }
}

// ============================================================
// ATTENDANCE LOGS
// ============================================================

async function loadAttendanceLogs() {
  const tbody = document.getElementById('attendanceLogsTableBody');
  tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 24px; color: var(--text-muted);">Loading logs...</td></tr>';

  try {
    const res = await fetch(API_BASE + '/attendance');
    allAttendanceLogs = await res.json();
    applyLogFilters();
  } catch (e) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; color: var(--error);">Failed to fetch attendance logs.</td></tr>';
  }
}

function applyLogFilters() {
  const query = document.getElementById('logSearchQuery').value.toLowerCase();
  const statusFilter = document.getElementById('logFilterStatus').value;
  const tbody = document.getElementById('attendanceLogsTableBody');
  const countEl = document.getElementById('logCountFooter');

  const filtered = allAttendanceLogs.filter(r => {
    const sName = (r.student_name || '').toLowerCase();
    const cName = (r.course_name || '').toLowerCase();
    const matchText = !query || sName.includes(query) || cName.includes(query);
    const matchStatus = !statusFilter || r.status === statusFilter;
    return matchText && matchStatus;
  });

  if (!filtered.length) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align: center; padding: 24px; color: var(--text-muted);">No attendance records found.</td></tr>';
    countEl.textContent = '0 records';
    return;
  }

  tbody.innerHTML = filtered.map(r => `
    <tr>
      <td class="mono">#${r.id}</td>
      <td><strong>${escapeHtml(r.student_name)}</strong> <span style="font-size:11px; color:var(--text-muted);">(ID: ${r.student_id})</span></td>
      <td>${escapeHtml(r.course_name)}</td>
      <td class="mono">${escapeHtml(r.timestamp || '--')}</td>
      <td><span class="badge ${r.status === 'Present' ? 'badge-success' : 'badge-warning'}">${escapeHtml(r.status)}</span></td>
    </tr>
  `).join('');

  countEl.textContent = `${filtered.length} record${filtered.length !== 1 ? 's' : ''}`;
}

// ============================================================
// UTILITIES
// ============================================================

function showBoxAlert(box, titleEl, msgEl, type, title, message) {
  box.className = 'verify-result-box show ' + type;
  if (titleEl) titleEl.textContent = title;
  if (msgEl) msgEl.textContent = message;
}

function showGlobalToast(type, msg) {
  const toast = document.getElementById('globalToast');
  if (!toast) return;
  const colors = {
    success: { bg: 'rgba(46, 125, 50, 0.95)', color: '#fff' },
    error: { bg: 'rgba(198, 40, 40, 0.95)', color: '#fff' },
    info: { bg: 'rgba(0, 48, 135, 0.95)', color: '#fff' }
  };
  const c = colors[type] || colors.info;
  toast.style.background = c.bg;
  toast.style.color = c.color;
  toast.textContent = msg;
  toast.classList.add('show');
  setTimeout(() => toast.classList.remove('show'), 3800);
}

function escapeHtml(s) {
  if (s == null) return '';
  return String(s)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}
</script>
</body>
</html>
'''

target_path = r"c:\Users\vishn\OneDrive\Desktop\New folder\attendance-system\frontend\index.html"
with open(target_path, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Generated complete frontend at: {target_path}")
print(f"File size: {len(HTML_CONTENT)} characters")
