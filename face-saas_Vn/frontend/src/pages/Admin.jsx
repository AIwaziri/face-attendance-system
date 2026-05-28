import { useEffect, useState } from "react";
import API from "../api";

export default function Admin() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const fetch = async () => {
      const res = await API.get("/attendance/admin");
      setLogs(res.data);
    };

    fetch();
    const interval = setInterval(fetch, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>👑 Admin Dashboard</h1>

      {logs.map((l, i) => (
        <div key={i} style={{ padding: 10, border: "1px solid #ddd" }}>
          <b>{l.name}</b> — {l.status} — {l.timestamp}
        </div>
      ))}
    </div>
  );
}