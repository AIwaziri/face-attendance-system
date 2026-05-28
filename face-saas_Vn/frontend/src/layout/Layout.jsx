import { Link } from "react-router-dom";

export default function Layout({ children }) {
  return (
    <div style={{ display: "flex", height: "100vh", fontFamily: "Arial" }}>

      {/* SIDEBAR */}
      <div style={{
        width: 220,
        background: "#111827",
        color: "white",
        padding: 20
      }}>
        <h2>🏢 HR SaaS</h2>

        <nav style={{ marginTop: 30 }}>
          <p><Link to="/" style={{ color: "white" }}>📊 Dashboard</Link></p>
          <p><Link to="/employees" style={{ color: "white" }}>👥 Employees</Link></p>
          <p><Link to="/analytics" style={{ color: "white" }}>📈 Analytics</Link></p>
        </nav>
      </div>

      {/* MAIN CONTENT */}
      <div style={{ flex: 1, padding: 20 }}>
        {children}
      </div>

    </div>
  );
}