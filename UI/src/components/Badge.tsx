import React from 'react';

interface BadgeProps {
  variant?: 'success' | 'warning' | 'danger' | 'info' | 'primary';
  children: React.ReactNode;
  dot?: boolean;
}

export const Badge: React.FC<BadgeProps> = ({ variant = 'primary', children, dot = false }) => {
  const variantClasses = {
    success: 'bg-emerald-500/15 text-accent-success border-emerald-500/30',
    warning: 'bg-amber-500/15 text-accent-warning border-amber-500/30',
    danger: 'bg-red-500/15 text-accent-danger border-red-500/30',
    info: 'bg-cyan-500/15 text-accent-info border-cyan-500/30',
    primary: 'bg-blue-500/15 text-accent-primary border-blue-500/30',
  };
  
  return (
    <span className={`inline-flex items-center gap-1 px-2 py-1 text-xs font-medium rounded border whitespace-nowrap ${variantClasses[variant]}`}>
      {dot && <span className="w-1.5 h-1.5 rounded-full bg-current" />}
      {children}
    </span>
  );
};
