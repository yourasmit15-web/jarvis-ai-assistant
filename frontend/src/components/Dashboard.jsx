import React, { useEffect, useState } from "react";
import { emergencyStop, getStatus } from "../services/api";

export default function Dashboard() {
  const [status, setStatus] = useState({ status: "loading", tools: [] });

  useEffect(() => {
    getStatus().then(({ data }) => setStatus(data)).catch(() => setStatus({ status: "error", tools: [] }));
  }, []);

  const onEmergencyStop = async () => {
    await emergencyStop();
    setStatus((prev) => ({ ...prev, status: "stopped" }));
  };

  return (
    <section className="card">
      <h2>Dashboard</h2>
      <p>Current status: {status.status}</p>
      <p>Connected tool modules: {status.tools?.length || 0}</p>
      <button type="button" className="danger" onClick={onEmergencyStop}>Emergency STOP</button>
    </section>
  );
}
