import React, { useEffect, useState } from "react";
import { getPermissions, updatePermission } from "../services/api";

export default function PermissionManager() {
  const [permissions, setPermissions] = useState({});

  const load = () => getPermissions().then(({ data }) => setPermissions(data));

  useEffect(() => {
    load();
  }, []);

  const toggle = async (permission, current) => {
    await updatePermission(permission, !current);
    await load();
  };

  return (
    <section className="card">
      <h2>Permission Manager</h2>
      <ul>
        {Object.entries(permissions).map(([permission, enabled]) => (
          <li key={permission}>
            <label>
              <input
                type="checkbox"
                checked={enabled}
                onChange={() => toggle(permission, enabled)}
              />
              {permission}
            </label>
          </li>
        ))}
      </ul>
    </section>
  );
}
