import useAttendanceSocket from "../hooks/useAttendanceSocket";
import { useMemo } from "react";

export default function Dashboard() {
  const logs = useAttendanceSocket();

  const stats = useMemo(() => {
    const total = logs.length;
    const ins = logs.filter(l => l.status === "IN").length;
    const outs = logs.filter(l => l.status === "OUT").length;

    return { total, ins, outs };
  }, [logs]);

  return (
    <div style={{ padding: 20, fontFamily: "Arial" }}>

      {/* HEADER */}
      <h2 style={{ fontSize: 28 }}>🏢 HR Dashboard</h2>
      <p style={{ color: "gray" }}>Real-time attendance monitoring</p>

      {/* KPI CARDS */}
      <div style={{ display: "flex", gap: 10, marginTop: 20 }}>
        <Card title="Total Events" value={stats.total} />
        <Card title="Check-ins (IN)" value={stats.ins} />
        <Card title="Check-outs (OUT)" value={stats.outs} />
      </div>

      {/* LIVE FEED */}
      <div style={{ marginTop: 30 }}>
        <h3>🔥 Live Activity</h3>

        <div style={{ marginTop: 10 }}>
          {logs.length === 0 && <p>No activity yet</p>}

          {logs.map((log, i) => (
            <div
              key={i}
              style={{
                padding: 10,
                marginBottom: 8,
                borderRadius: 8,
                background: "#f5f5f5",
                display: "flex",
                justifyContent: "space-between"
              }}
            >
              <span>👤 {log.name}</span>
              <span>{log.status === "IN" ? "🟢 IN" : "🔴 OUT"}</span>
              <span style={{ color: "gray" }}>{log.timestamp}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

/* KPI CARD COMPONENT */
function Card({ title, value }) {
  return (
    <div
      style={{
        flex: 1,
        background: "white",
        padding: 15,
        borderRadius: 10,
        boxShadow: "0 2px 10px rgba(0,0,0,0.1)"
      }}
    >
      <p style={{ color: "gray", margin: 0 }}>{title}</p>
      <h3 style={{ margin: 0, fontSize: 22 }}>{value}</h3>
    </div>
  );
}