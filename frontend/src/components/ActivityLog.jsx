import React, { useEffect, useState } from "react";
import { getActivityLog } from "../services/api";

const ActivityLog = () => {
  const [items, setItems] = useState([]);

  useEffect(() => {
    getActivityLog().then((data) => setItems(data.items || []));
  }, []);

  return (
    <section className="card">
      <h2>Activity Log</h2>
      <ul>
        {items.map((item, index) => (
          <li key={`${item.timestamp}-${index}`}>
            {item.timestamp} - {item.event_type}
          </li>
        ))}
      </ul>
    </section>
  );
};

export default ActivityLog;
