import { useEffect } from "react";

export default function LiveFeed() {
  useEffect(() => {
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onmessage = (msg) => {
      console.log("LIVE:", msg.data);
    };

    return () => ws.close();
  }, []);

  return <div>Live Feed Running...</div>;
}