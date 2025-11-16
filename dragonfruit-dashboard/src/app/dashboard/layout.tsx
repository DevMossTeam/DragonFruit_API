// src/app/dashboard/layout.tsx
'use client';

import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';
import { useState } from 'react';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleToggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="flex flex-col min-h-screen bg-gray-100">
      {/* Top Navbar */}
      <Navbar onToggleSidebar={handleToggleSidebar} />

      {/* Main Content with Sidebar */}
      <div className="flex flex-1 pt-16">
        {/* Sidebar */}
        <Sidebar />

        {/* Page Content */}
        <main className="flex-1 p-6 md:ml-64 w-full overflow-y-auto">
          {children}
        </main>
      </div>
    </div>
  );
}