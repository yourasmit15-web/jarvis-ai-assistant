import React, { useEffect, useState } from "react";
import { getActivityLog } from "../services/api";
import { formatDate } from "../utils/helpers";

export default function ActivityLog() {
  const [events, setEvents] = useState([]);

  useEffect(() => {
    getActivityLog().then(({ data }) => setEvents(data)).catch(() => setEvents([]));
  }, []);

  return (
    <section className="card">
      <h2>Activity Log</h2>
      <ul>
        {events.map((event, index) => (
          <li key={index}>
            <strong>{event.type}</strong> - {formatDate(event.timestamp)}
          </li>
        ))}
      </ul>
    </section>
  );
}
