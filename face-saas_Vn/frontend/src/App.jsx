import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { useEffect, useState } from "react";

import API from "./api";
import CameraCapture from "./components/CameraCapture";
import Employees from "./pages/Employees";
import Analytics from "./pages/Analytics";
import Layout from "./layout/Layout";
import Login from "./pages/Login";
import Admin from "./pages/Admin";
import EmployeeDashboard from "./pages/EmployeeDashboard";

function Dashboard() {
  const [attendance, setAttendance] = useState([]);

  const fetchAttendance = async () => {
    try {
      const res = await API.get("/attendance/");
      setAttendance(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  useEffect(() => {
    fetchAttendance();

    const interval = setInterval(fetchAttendance, 3000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div>
      <h1>📊 Dashboard</h1>

      <CameraCapture />

      <h2>Attendance Logs</h2>

      {attendance.map((item, i) => (
        <div
          key={i}
          style={{
            padding: 10,
            borderBottom: "1px solid #ddd",
          }}
        >
          👤 {item.name} | {item.status} | 🕒 {item.timestamp}
        </div>
      ))}
    </div>
  );
}

export default function App() {
  return (
    <Router>
      <Layout>
        <Routes>
          <Route path="/" element={<Dashboard />} />

          <Route path="/login" element={<Login />} />

          <Route path="/admin" element={<Admin />} />

          <Route
            path="/employee"
            element={<EmployeeDashboard />}
          />

          <Route
            path="/employees"
            element={<Employees />}
          />

          <Route
            path="/analytics"
            element={<Analytics />}
          />
        </Routes>
      </Layout>
    </Router>
  );
}