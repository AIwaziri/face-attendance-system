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
    <div style={styles.page}>

      {/* NAVBAR */}
      <div style={styles.nav}>
        <h2 style={{ margin: 0 }}>🏢 AiWaziri HR SaaS</h2>
        <span style={{ fontSize: 12, color: "#666" }}>Live Attendance System</span>
      </div>

      {/* KPI SECTION */}
      <div style={styles.kpiGrid}>
        <KPI title="Total Events" value={stats.total} />
        <KPI title="Check-ins" value={stats.ins} />
        <KPI title="Check-outs" value={stats.outs} />
      </div>

      {/* MAIN CONTENT */}
      <div style={styles.content}>

        {/* LIVE FEED */}
        <div style={styles.card}>
          <h3>🔥 Live Activity Feed</h3>

          {logs.length === 0 ? (
            <p style={{ color: "#888" }}>No activity yet</p>
          ) : (
            <div style={styles.feed}>
              {logs.map((log, i) => (
                <div key={i} style={styles.feedItem}>
                  <div>
                    <div style={{ fontWeight: "bold" }}>👤 {log.name}</div>
                    <div style={{ fontSize: 12, color: "#777" }}>
                      {log.timestamp}
                    </div>
                  </div>

                  <span
                    style={{
                      ...styles.badge,
                      background: log.status === "IN" ? "#d1fae5" : "#fee2e2",
                      color: log.status === "IN" ? "#065f46" : "#991b1b"
                    }}
                  >
                    {log.status}
                  </span>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

/* KPI COMPONENT */
function KPI({ title, value }) {
  return (
    <div style={styles.kpiCard}>
      <div style={{ fontSize: 12, color: "#666" }}>{title}</div>
      <div style={{ fontSize: 24, fontWeight: "bold" }}>{value}</div>
    </div>
  );
}

/* STYLES */
const styles = {
  page: {
    padding: 20,
    fontFamily: "Arial",
    background: "#f6f7fb",
    minHeight: "100vh"
  },

  nav: {
    background: "white",
    padding: 15,
    borderRadius: 10,
    marginBottom: 20,
    boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
  },

  kpiGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(3, 1fr)",
    gap: 10,
    marginBottom: 20
  },

  kpiCard: {
    background: "white",
    padding: 15,
    borderRadius: 10,
    boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
  },

  content: {
    display: "grid",
    gridTemplateColumns: "1fr",
    gap: 20
  },

  card: {
    background: "white",
    padding: 15,
    borderRadius: 10,
    boxShadow: "0 2px 8px rgba(0,0,0,0.05)"
  },

  feed: {
    marginTop: 10,
    maxHeight: 400,
    overflowY: "auto"
  },

  feedItem: {
    display: "flex",
    justifyContent: "space-between",
    padding: 12,
    borderBottom: "1px solid #eee"
  },

  badge: {
    padding: "4px 10px",
    borderRadius: 20,
    fontSize: 12,
    fontWeight: "bold"
  }
};