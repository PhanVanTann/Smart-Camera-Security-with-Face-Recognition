import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'success' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  children: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
  variant = 'primary',
  size = 'md',
  children,
  className = '',
  ...props
}) => {
  const baseClasses = 'inline-flex items-center justify-center gap-2 font-medium rounded-md transition-all duration-150 cursor-pointer border-none outline-none whitespace-nowrap disabled:opacity-50 disabled:cursor-not-allowed';
  
  const variantClasses = {
    primary: 'bg-accent-primary text-white hover:bg-blue-600 hover:shadow-glow hover:-translate-y-px active:translate-y-0',
    secondary: 'bg-bg-tertiary text-text-primary border border-border-secondary hover:bg-bg-hover hover:border-border-hover',
    success: 'bg-accent-success text-white hover:bg-emerald-600 hover:shadow-glow-success hover:-translate-y-px active:translate-y-0',
    danger: 'bg-accent-danger text-white hover:bg-red-600 hover:shadow-glow-danger hover:-translate-y-px active:translate-y-0',
  };
  
  const sizeClasses = {
    sm: 'px-3 py-1 text-xs',
    md: 'px-6 py-2 text-sm',
    lg: 'px-8 py-3 text-base',
  };
  
  return (
    <button
      className={`${baseClasses} ${variantClasses[variant]} ${sizeClasses[size]} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
};
