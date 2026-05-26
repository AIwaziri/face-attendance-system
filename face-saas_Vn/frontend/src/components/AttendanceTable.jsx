export default function AttendanceTable({ data }) {
  return (
    <div>
      {data.map((d, i) => (
        <p key={i}>{d.name} - {d.status}</p>
      ))}
    </div>
  );
}