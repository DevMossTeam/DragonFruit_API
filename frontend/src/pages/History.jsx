import { useEffect, useState } from "react";
import axios from "axios";
import Chart from "../components/Chart";

export default function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    axios.get("http://127.0.0.1:8000/api/grading/history").then((res) => {
      setHistory(res.data);
    });
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold mb-2">Riwayat Grading</h1>
      <Chart data={history.map(h => ({
        ...h,
        timestamp: new Date(h.timestamp).toLocaleTimeString()
      }))} />
      <table border="1" cellPadding="6" style={{ marginTop: 20, width: "100%" }}>
        <thead>
          <tr>
            <th>Waktu</th>
            <th>Gambar</th>
            <th>Grade</th>
            <th>Confidence</th>
          </tr>
        </thead>
        <tbody>
          {history.map((item) => (
            <tr key={item.id}>
              <td>{new Date(item.timestamp).toLocaleString()}</td>
              <td>{item.image_name}</td>
              <td>{item.grade}</td>
              <td>{item.confidence}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
