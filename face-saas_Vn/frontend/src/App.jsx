import { useEffect, useState } from "react";
import API from "./api";
import CameraCapture from "./components/CameraCapture";

export default function App() {
  const [attendance, setAttendance] = useState([]);

  const fetchAttendance = async () => {
    try {
      const res = await API.get("/attendance/");
      console.log("ATTENDANCE DATA:", res.data);
      setAttendance(res.data);
    } catch (err) {
      console.log("ERROR:", err);
    }
  };

  useEffect(() => {
    fetchAttendance();

    const interval = setInterval(() => {
      fetchAttendance();
    }, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>
      <h1>AiWaziri FaceID Attendance System SaaS</h1>

      <CameraCapture />

      <h2>Attendance Logs</h2>

      {attendance.length === 0 ? (
        <p>No attendance records yet</p>
      ) : (
        attendance.map((item, index) => (
          <div
            key={index}
            style={{
              padding: 10,
              margin: 10,
              border: "1px solid #ccc",
              borderRadius: 5
            }}
          >
            <b>👤 {item.name}</b>
            <br />
            📌 {item.status}
            <br />
            🕒 {item.timestamp}
          </div>
        ))
      )}
    </div>
  );
}