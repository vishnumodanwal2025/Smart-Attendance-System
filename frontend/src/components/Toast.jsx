import React from 'react';

export default function Toast({ toast }) {
  if (!toast || !toast.show) return null;

  const bgMap = {
    success: 'rgba(46, 125, 50, 0.95)',
    error: 'rgba(198, 40, 40, 0.95)',
    info: 'rgba(0, 48, 135, 0.95)',
    warning: 'rgba(230, 81, 0, 0.95)'
  };

  const bg = bgMap[toast.type] || bgMap.info;

  return (
    <div
      id="globalToast"
      className="show"
      style={{
        background: bg,
        color: '#ffffff'
      }}
    >
      {toast.message}
    </div>
  );
}
