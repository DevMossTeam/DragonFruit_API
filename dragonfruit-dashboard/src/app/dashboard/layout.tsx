// src/app/dashboard/layout.tsx
'use client';

import Sidebar from './components/Sidebar';
import Navbar from './components/Navbar';

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-gray-100">
      {/* Navbar*/}
      <div className="w-64 bg-white shadow-md">
        <Navbar/>
      </div>

      {/* Main Content Area */}
      <div className="flex flex-col flex-1">
        {/* Sidebar */}
        <Sidebar />

        {/* Page Content */}
        <main className="flex-1 p-6 mt-16">
          {children}
        </main>
      </div>
    </div>
  );
}