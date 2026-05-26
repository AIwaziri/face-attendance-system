import { useEffect, useState } from "react";
import API from "../api";

export default function Users() {
  const [users, setUsers] = useState([]);

  const fetchUsers = async () => {
    const res = await API.get("/users/");
    setUsers(res.data);
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Registered Users</h1>

      {users.map((u) => (
        <div key={u.id} style={{ margin: 10 }}>
          👤 {u.name}
        </div>
      ))}
    </div>
  );
}