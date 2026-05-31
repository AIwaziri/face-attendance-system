import { useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api";

export default function Login() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const login = async () => {
    try {
      setLoading(true);

      const res = await API.post(
        `/auth/login?name=${encodeURIComponent(
          name
        )}&password=${encodeURIComponent(password)}`
      );

      localStorage.setItem(
        "token",
        res.data.access_token
      );

      localStorage.setItem(
        "role",
        res.data.role
      );

      alert("Login successful!");

      if (res.data.role === "admin") {
        navigate("/admin");
      } else {
        navigate("/employee");
      }

    } catch (err) {
      console.error(err);

      alert(
        err?.response?.data?.detail ||
        "Login failed"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: "400px",
        margin: "50px auto",
        padding: "20px",
        border: "1px solid #ddd",
        borderRadius: "10px"
      }}
    >
      <h2>🔐 Login</h2>

      <input
        type="text"
        placeholder="Username"
        value={name}
        onChange={(e) => setName(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px"
        }}
      />

      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          marginBottom: "10px"
        }}
      />

      <button
        onClick={login}
        disabled={loading}
        style={{
          width: "100%",
          padding: "10px",
          cursor: "pointer"
        }}
      >
        {loading ? "Logging in..." : "Login"}
      </button>
    </div>
  );
}