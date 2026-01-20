import React from 'react';

interface CardProps {
  children: React.ReactNode;
  className?: string;
  title?: string;
  action?: React.ReactNode;
}

export const Card: React.FC<CardProps> = ({ children, className = '', title, action }) => {
  return (
    <div className={`bg-bg-card rounded-lg p-6 border border-border-primary shadow-md transition-all duration-250 hover:border-border-secondary hover:shadow-lg hover:-translate-y-0.5 ${className}`}>
      {(title || action) && (
        <div className="flex items-center justify-between mb-4 pb-4 border-b border-border-primary">
          {title && <h3 className="text-lg font-semibold text-text-primary">{title}</h3>}
          {action}
        </div>
      )}
      <div className="text-text-secondary">{children}</div>
    </div>
  );
};
