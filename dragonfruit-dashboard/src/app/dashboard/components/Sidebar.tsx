// src/app/components/Sidebar.tsx
'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faTachometerAlt, faChartLine, faUsers, faCog, faSignOutAlt } from '@fortawesome/free-solid-svg-icons';

export default function Sidebar() {
  const [isOpen, setIsOpen] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Listen for custom events from navbar
    const handleToggle = () => {
      setIsOpen((prev) => !prev);
    };

    window.addEventListener('toggleSidebar', handleToggle);
    return () => window.removeEventListener('toggleSidebar', handleToggle);
  }, []);

  const handleLogout = () => {
    // Clear user from localStorage
    localStorage.removeItem('user');
    // Redirect to login
    router.push('/login');
  };

  const menuItems = [
    { href: '/dashboard', label: 'Dashboard', icon: faTachometerAlt },
    { href: '/dashboard/graph', label: 'Analytics', icon: faChartLine },
    { href: '/dashboard/users', label: 'Users', icon: faUsers },
    { href: '/dashboard/settings', label: 'Settings', icon: faCog },
  ];

  return (
    <>
      {/* Desktop Sidebar - Always visible */}
      <aside className="hidden md:flex md:fixed md:left-0 md:top-16 md:z-40 md:w-64 md:h-[calc(100vh-64px)] md:flex-col md:border-r md:border-gray-200 md:bg-white">
        <div className="px-3 py-4 overflow-y-auto flex-1">
          <ul className="space-y-2 font-medium">
            {menuItems.map((item) => (
              <li key={item.href}>
                <a
                  href={item.href}
                  className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 transition-colors duration-150 group"
                >
                  <FontAwesomeIcon
                    icon={item.icon}
                    className="w-5 h-5 text-gray-500 group-hover:text-gray-900 transition-colors"
                  />
                  <span className="ms-3">{item.label}</span>
                </a>
              </li>
            ))}
          </ul>
        </div>

        {/* Logout Button */}
        <div className="border-t border-gray-200 px-3 py-4">
          <button
            onClick={handleLogout}
            className="w-full flex items-center p-2 text-gray-900 rounded-lg hover:bg-red-50 transition-colors duration-150 group"
          >
            <FontAwesomeIcon
              icon={faSignOutAlt}
              className="w-5 h-5 text-gray-500 group-hover:text-red-600 transition-colors"
            />
            <span className="ms-3 group-hover:text-red-600 transition-colors">Logout</span>
          </button>
        </div>
      </aside>

      {/* Mobile Sidebar - Toggleable */}
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-30 md:hidden mt-16"
          onClick={() => setIsOpen(false)}
        />
      )}

      <aside
        className={`fixed left-0 top-16 z-40 w-64 h-[calc(100vh-64px)] bg-white border-r border-gray-200 md:hidden transform transition-transform duration-300 ease-in-out ${
          isOpen ? 'translate-x-0 shadow-lg' : '-translate-x-full'
        }`}
      >
        <div className="px-3 py-4 overflow-y-auto h-full flex flex-col">
          <ul className="space-y-2 font-medium flex-1">
            {menuItems.map((item) => (
              <li key={item.href}>
                <a
                  href={item.href}
                  onClick={() => setIsOpen(false)}
                  className="flex items-center p-2 text-gray-900 rounded-lg hover:bg-gray-100 transition-colors duration-150 group"
                >
                  <FontAwesomeIcon
                    icon={item.icon}
                    className="w-5 h-5 text-gray-500 group-hover:text-gray-900 transition-colors"
                  />
                  <span className="ms-3">{item.label}</span>
                </a>
              </li>
            ))}
          </ul>

          {/* Logout Button */}
          <div className="border-t border-gray-200 pt-4">
            <button
              onClick={() => {
                setIsOpen(false);
                handleLogout();
              }}
              className="w-full flex items-center p-2 text-gray-900 rounded-lg hover:bg-red-50 transition-colors duration-150 group"
            >
              <FontAwesomeIcon
                icon={faSignOutAlt}
                className="w-5 h-5 text-gray-500 group-hover:text-red-600 transition-colors"
              />
              <span className="ms-3 group-hover:text-red-600 transition-colors">Logout</span>
            </button>
          </div>
        </div>
      </aside>

      {/* Script to expose sidebar toggle globally */}
      <script
        dangerouslySetInnerHTML={{
          __html: `
            if (typeof window !== 'undefined') {
              window.addEventListener('sidebar-toggle', function() {
                const event = new Event('toggleSidebar');
                window.dispatchEvent(event);
              });
            }
          `,
        }}
      />
    </>
  );
}