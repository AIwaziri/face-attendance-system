import { useEffect, useState } from "react";
import {
  LineChart, Line, XAxis, YAxis, Tooltip, CartesianGrid, BarChart, Bar
} from "recharts";
import API from "../api";

export default function Analytics() {
  const [daily, setDaily] = useState({});
  const [weekly, setWeekly] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      const d = await API.get("/analytics/daily");
      const w = await API.get("/analytics/weekly");

      setDaily(d.data);
      setWeekly(w.data);
    };

    fetchData();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>📊 Analytics Dashboard</h1>

      {/* KPI */}
      <div style={{ display: "flex", gap: 10 }}>
        <Card title="Total Today" value={daily.total} />
        <Card title="Check-ins" value={daily.in} />
        <Card title="Check-outs" value={daily.out} />
      </div>

      {/* WEEKLY CHART */}
      <h3 style={{ marginTop: 30 }}>Weekly Attendance</h3>

      <LineChart width={600} height={300} data={weekly}>
        <XAxis dataKey="date" />
        <YAxis />
        <Tooltip />
        <CartesianGrid />
        <Line type="monotone" dataKey="total" stroke="#4f46e5" />
      </LineChart>
    </div>
  );
}

function Card({ title, value }) {
  return (
    <div style={{
      padding: 15,
      background: "#fff",
      borderRadius: 10,
      boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
    }}>
      <h4>{title}</h4>
      <h2>{value}</h2>
    </div>
  );
}