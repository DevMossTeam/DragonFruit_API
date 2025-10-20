import { useState, useEffect } from "react";
import axios from "axios";

export default function DeviceStatus() {
  const [status, setStatus] = useState([]);

  useEffect(() => {
    // Simulasi data perangkat
    setStatus([
      { id: "IoT-01", online: true },
      { id: "IoT-02", online: false },
    ]);
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold">Status Perangkat IoT</h1>
      <ul>
        {status.map((d) => (
          <li key={d.id}>
            {d.id} — {d.online ? "🟢 Online" : "🔴 Offline"}
          </li>
        ))}
      </ul>
    </div>
  );
}
