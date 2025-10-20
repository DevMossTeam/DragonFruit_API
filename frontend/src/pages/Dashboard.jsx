import { useState } from "react";
import axios from "axios";

export default function Dashboard() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    const formData = new FormData();
    formData.append("file", file);
    const res = await axios.post("http://127.0.0.1:8000/api/grading/analyze", formData);
    setResult(res.data);
  };

  return (
    <div className="p-6">
      <h1 className="text-xl font-bold">DragonEye - Grading Buah Naga</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload}>Upload</button>
      {result && (
        <div>
          <p>Grade: {result.grade}</p>
          <p>Confidence: {result.confidence}</p>
        </div>
      )}
    </div>
  );
}
