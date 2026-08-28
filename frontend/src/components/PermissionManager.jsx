import React, { useEffect, useState } from "react";
import { getPermissions, updatePermissions } from "../services/api";

const PermissionManager = () => {
  const [permissions, setPermissions] = useState({});

  useEffect(() => {
    getPermissions().then((data) => setPermissions(data.permissions));
  }, []);

  const toggle = async (key) => {
    const updated = { ...permissions, [key]: !permissions[key] };
    setPermissions(updated);
    await updatePermissions({ [key]: updated[key] });
  };

  return (
    <section className="card">
      <h2>Permissions</h2>
      <ul>
        {Object.entries(permissions).map(([key, enabled]) => (
          <li key={key}>
            <label>
              <input type="checkbox" checked={enabled} onChange={() => toggle(key)} /> {key}
            </label>
          </li>
        ))}
      </ul>
    </section>
  );
};

export default PermissionManager;
