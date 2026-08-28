import React, { useEffect, useState } from "react";
import { getStatus, emergencyStop } from "../services/api";

const Dashboard = () => {
  const [status, setStatus] = useState({ status: "loading", registered_tools: [] });

  const refresh = async () => {
    const next = await getStatus();
    setStatus(next);
  };

  useEffect(() => {
    refresh();
  }, []);

  const toggleStop = async () => {
    await emergencyStop(status.status !== "stopped");
    await refresh();
  };

  return (
    <section className="card">
      <h2>Status Dashboard</h2>
      <p>System: {status.status}</p>
      <p>Tools: {status.registered_tools?.length || 0}</p>
      <button type="button" className="danger" onClick={toggleStop}>Emergency STOP</button>
    </section>
  );
};

export default Dashboard;
