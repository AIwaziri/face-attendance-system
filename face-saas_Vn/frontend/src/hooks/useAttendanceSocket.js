import { useEffect, useState } from "react";

export default function useAttendanceSocket() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    const ws = new WebSocket("ws://127.0.0.1:8000/ws/attendance");

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setLogs((prev) => [data, ...prev]);
    };

    return () => ws.close();
  }, []);

  return logs;
}