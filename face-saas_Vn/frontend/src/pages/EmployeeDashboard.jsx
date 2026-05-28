import { useEffect, useState } from "react";
import API from "../api";

export default function EmployeeDashboard() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetch = async () => {
      const res = await API.get("/attendance/me");
      setLogs(res.data);
    };

    fetch();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>👤 My Attendance</h1>

      {logs.map((l, i) => (
        <div key={i}>
          {l.status} - {l.timestamp}
        </div>
      ))}
    </div>
  );
}