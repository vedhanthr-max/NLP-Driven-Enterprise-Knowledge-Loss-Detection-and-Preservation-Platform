import React from 'react';
import { ShieldAlert, ShieldCheck, AlertTriangle, Flame } from 'lucide-react';

export default function RiskBadge({ level, score }) {
  const lvl = (level || 'medium').toLowerCase();
  
  const icons = {
    low: <ShieldCheck size={14} />,
    medium: <ShieldAlert size={14} />,
    high: <AlertTriangle size={14} />,
    critical: <Flame size={14} />
  };

  return (
    <span className={`badge badge-${lvl}`}>
      {icons[lvl] || <ShieldAlert size={14} />}
      {lvl.toUpperCase()} {score !== undefined && score !== null ? `(${Math.round(score)})` : ''}
    </span>
  );
}
