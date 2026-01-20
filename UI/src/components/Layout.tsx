import React from 'react';
import { Sidebar } from './Sidebar';
import { Header } from './Header';

interface LayoutProps {
  children: React.ReactNode;
  title: string;
}

export const Layout: React.FC<LayoutProps> = ({ children, title }) => {
  return (
    <div className="flex min-h-screen bg-bg-primary">
      <Sidebar />
      <Header title={title} />
      <main className="flex-1 ml-64 mt-[70px] p-8 min-h-[calc(100vh-70px)]">
        {children}
      </main>
    </div>
  );
};
