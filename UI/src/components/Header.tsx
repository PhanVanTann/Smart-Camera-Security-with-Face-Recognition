import React from 'react';

interface HeaderProps {
  title: string;
}

export const Header: React.FC<HeaderProps> = ({ title }) => {
  return (
    <header className="fixed top-0 left-64 right-0 h-[70px] bg-bg-secondary border-b border-border-primary px-8 flex items-center justify-between z-40">
      {/* Left Side */}
      <div className="flex items-center gap-6">
        <h1 className="text-2xl font-bold text-text-primary">{title}</h1>
      </div>

      {/* Right Side */}
      <div className="flex items-center gap-6">
        {/* Search */}
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-text-tertiary text-sm">🔍</span>
          <input
            type="text"
            className="pl-10 pr-4 py-2 bg-bg-tertiary border border-border-primary rounded-md text-text-primary text-sm w-72 focus:border-accent-primary focus:ring-2 focus:ring-accent-primary/20 focus:outline-none transition-all"
            placeholder="Search..."
          />
        </div>

        {/* Actions */}
        <div className="flex items-center gap-3">
          <button className="relative w-10 h-10 flex items-center justify-center bg-bg-tertiary rounded-md text-text-secondary text-lg hover:bg-bg-hover hover:text-text-primary transition-all">
            🔔
            <span className="absolute -top-1 -right-1 w-[18px] h-[18px] bg-accent-danger text-white text-[10px] font-semibold rounded-full flex items-center justify-center border-2 border-bg-secondary">
              3
            </span>
          </button>
          <button className="w-10 h-10 flex items-center justify-center bg-bg-tertiary rounded-md text-text-secondary text-lg hover:bg-bg-hover hover:text-text-primary transition-all">
            ⚙️
          </button>
        </div>
      </div>
    </header>
  );
};
