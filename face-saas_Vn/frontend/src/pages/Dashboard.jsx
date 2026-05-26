import { useEffect, useState } from "react";

export default function Dashboard() {
  const [data, setData] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/attendance/")
      .then(res => res.json())
      .then(setData);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Face Attendance SaaS Dashboard</h1>

      {data.map((item, i) => (
        <div key={i} style={{ margin: 10 }}>
          👤 {item.name} | {item.status} | {item.timestamp}
        </div>
      ))}
    </div>
  );
}