import React from 'react';
import { Link, useLocation } from 'react-router-dom';

interface NavItem {
  path: string;
  label: string;
  icon: string;
}

const navItems: NavItem[] = [
  { path: '/camera-monitor', label: 'Camera Monitor', icon: '📹' },
  { path: '/residents', label: 'Residents', icon: '👥' },
];

export const Sidebar: React.FC = () => {
  const location = useLocation();

  return (
    <aside className="fixed left-0 top-0 bottom-0 w-64 bg-bg-secondary border-r border-border-primary p-6 flex flex-col gap-6 z-50 overflow-y-auto">
      {/* Logo */}
      <div className="flex items-center gap-3 p-3 mb-4">
        <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-lg flex items-center justify-center text-xl">
          🔒
        </div>
        <span className="text-lg font-bold text-text-primary">SecureVision</span>
      </div>

      {/* Navigation */}
      <nav className="flex flex-col gap-1">
        {navItems.map((item) => (
          <Link
            key={item.path}
            to={item.path}
            className={`flex items-center gap-3 px-3 py-3 rounded-md text-sm font-medium transition-all duration-150 ${
              location.pathname === item.path
                ? 'bg-accent-primary text-white shadow-glow'
                : 'text-text-secondary hover:bg-bg-hover hover:text-text-primary'
            }`}
          >
            <span className="text-lg w-5 text-center">{item.icon}</span>
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      {/* User Section */}
      <div className="mt-auto pt-6 border-t border-border-primary">
        <div className="flex items-center gap-3 p-3 rounded-md bg-bg-tertiary cursor-pointer transition-all hover:bg-bg-hover">
          <div className="w-9 h-9 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-semibold text-sm">
            AD
          </div>
          <div className="flex-1">
            <div className="text-sm font-semibold text-text-primary">Admin User</div>
            <div className="text-xs text-text-tertiary">Security Operator</div>
          </div>
        </div>
      </div>
    </aside>
  );
};
