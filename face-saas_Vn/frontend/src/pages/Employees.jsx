import { useEffect, useState } from "react";
import API from "../api";

export default function Employees() {
  const [employees, setEmployees] = useState([]);
  const [name, setName] = useState("");

  const load = async () => {
    const res = await API.get("/employees/");
    setEmployees(res.data);
  };

  useEffect(() => {
    load();
  }, []);

  const addEmployee = async () => {
    await API.post(`/employees/add?name=${name}`);
    setName("");
    load();
  };

  const deleteEmployee = async (id) => {
    await API.delete(`/employees/${id}`);
    load();
  };

  return (
    <div style={{ padding: 20 }}>
      <h2>👥 Employee Management</h2>

      {/* ADD */}
      <div style={{ marginBottom: 20 }}>
        <input
          placeholder="Employee name"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
        <button onClick={addEmployee}>Add</button>
      </div>

      {/* LIST */}
      {employees.map((emp) => (
        <div
          key={emp.id}
          style={{
            display: "flex",
            justifyContent: "space-between",
            padding: 10,
            border: "1px solid #ddd",
            marginBottom: 8
          }}
        >
          <span>👤 {emp.name}</span>
          <span>{emp.role}</span>
          <button onClick={() => deleteEmployee(emp.id)}>Delete</button>
        </div>
      ))}
    </div>
  );
}