// src/app/components/Sidebar.tsx
export default function Sidebar() {
  return (
    <aside className="w-64 bg-white shadow-md p-4">
      <h1 className="text-xl font-bold mb-6">Admin Panel</h1>
      <nav>
        <ul className="space-y-2">
          <li><a href="/" className="block p-2 hover:bg-gray-100 rounded">Dashboard</a></li>
          <li><a href="/users" className="block p-2 hover:bg-gray-100 rounded">Users</a></li>
        </ul>
      </nav>
    </aside>
  );
}