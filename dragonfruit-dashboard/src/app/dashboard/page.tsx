// src/app/dashboard/page.tsx
export default function DashboardPage() {
  // Data dummy — nanti bisa diganti dengan API/fetch
  const stats = {
    totalGraded: 428,
    gradeA: 65,
    gradeB: 28,
    gradeC: 7,
    machineStatus: 'online',
    lastScan: '2 menit yang lalu',
  };

  return (
    <div className="p-6 space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-bold text-gray-800">Dashboard</h1>
        <p className="mt-1 text-gray-600">
          Sistem Grading Buah Naga Super Merah – Pantau proses grading real-time dari mesin IoT.
        </p>
      </div>

      {/* Statistik Utama */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        {/* Total Graded */}
        <div className="bg-white rounded-xl shadow p-5 border-l-4 border-blue-500">
          <p className="text-sm font-medium text-gray-500">Total Graded Hari Ini</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{stats.totalGraded} buah</p>
        </div>

        {/* Grade A */}
        <div className="bg-white rounded-xl shadow p-5 border-l-4 border-green-500">
          <p className="text-sm font-medium text-gray-500">Grade A</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{stats.gradeA}%</p>
        </div>

        {/* Grade B */}
        <div className="bg-white rounded-xl shadow p-5 border-l-4 border-yellow-500">
          <p className="text-sm font-medium text-gray-500">Grade B</p>
          <p className="text-2xl font-bold text-gray-900 mt-1">{stats.gradeB}%</p>
        </div>

        {/* Status Mesin */}
        <div className="bg-white rounded-xl shadow p-5 border-l-4 border-green-500">
          <p className="text-sm font-medium text-gray-500">Status Mesin IoT</p>
          <div className="flex items-center mt-1">
            <span className="inline-flex w-3 h-3 rounded-full bg-green-500 mr-2"></span>
            <span className="font-medium text-gray-900">
              {stats.machineStatus === 'online' ? 'Online' : 'Offline'}
            </span>
          </div>
          <p className="text-xs text-gray-500 mt-1">{stats.lastScan}</p>
        </div>
      </div>

      {/* Grafik & Aktivitas Terbaru */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Distribusi Grade (Pie Chart Placeholder) */}
        <div className="bg-white rounded-xl shadow p-5 lg:col-span-1">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">Distribusi Grade</h2>
          <div className="space-y-3">
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">Grade A</span>
                <span className="font-medium">{stats.gradeA}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-green-500 h-2 rounded-full"
                  style={{ width: `${stats.gradeA}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">Grade B</span>
                <span className="font-medium">{stats.gradeB}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-yellow-500 h-2 rounded-full"
                  style={{ width: `${stats.gradeB}%` }}
                ></div>
              </div>
            </div>
            <div>
              <div className="flex justify-between text-sm mb-1">
                <span className="text-gray-600">Grade C</span>
                <span className="font-medium">{stats.gradeC}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-red-500 h-2 rounded-full"
                  style={{ width: `${stats.gradeC}%` }}
                ></div>
              </div>
            </div>
          </div>
        </div>

        {/* Aktivitas Terbaru */}
        <div className="bg-white rounded-xl shadow p-5 lg:col-span-2">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg font-semibold text-gray-800">Aktivitas Terbaru</h2>
            <a href="/logs" className="text-sm text-blue-600 hover:underline">Lihat semua</a>
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm text-gray-600">
              <thead>
                <tr className="border-b">
                  <th className="py-2 text-left">Waktu</th>
                  <th className="py-2 text-left">ID Buah</th>
                  <th className="py-2 text-left">Grade</th>
                  <th className="py-2 text-left">Ukuran (cm)</th>
                </tr>
              </thead>
              <tbody>
                <tr className="border-b hover:bg-gray-50">
                  <td className="py-2">10:42</td>
                  <td className="py-2">DN-0428</td>
                  <td className="py-2">
                    <span className="px-2 py-0.5 text-xs bg-green-100 text-green-800 rounded-full">A</span>
                  </td>
                  <td className="py-2">12.3</td>
                </tr>
                <tr className="border-b hover:bg-gray-50">
                  <td className="py-2">10:41</td>
                  <td className="py-2">DN-0427</td>
                  <td className="py-2">
                    <span className="px-2 py-0.5 text-xs bg-yellow-100 text-yellow-800 rounded-full">B</span>
                  </td>
                  <td className="py-2">11.7</td>
                </tr>
                <tr className="border-b hover:bg-gray-50">
                  <td className="py-2">10:40</td>
                  <td className="py-2">DN-0426</td>
                  <td className="py-2">
                    <span className="px-2 py-0.5 text-xs bg-green-100 text-green-800 rounded-full">A</span>
                  </td>
                  <td className="py-2">12.8</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      {/* Panel Kontrol Cepat */}
      <div className="bg-white rounded-xl shadow p-5">
        <h2 className="text-lg font-semibold text-gray-800 mb-3">Kontrol Mesin</h2>
        <div className="flex flex-wrap gap-3">
          <button className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700">
            Mulai Grading
          </button>
          <button className="px-4 py-2 bg-red-600 text-white rounded-lg text-sm font-medium hover:bg-red-700">
            Hentikan
          </button>
          <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50">
            Kalibrasi Kamera
          </button>
          <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded-lg text-sm font-medium hover:bg-gray-50">
            Lihat Log IoT
          </button>
        </div>
      </div>
    </div>
  );
}