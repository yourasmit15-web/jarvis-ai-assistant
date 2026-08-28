import React from "react";
import ChatInterface from "./components/ChatInterface";
import Dashboard from "./components/Dashboard";
import PermissionManager from "./components/PermissionManager";
import MemoryViewer from "./components/MemoryViewer";
import ActivityLog from "./components/ActivityLog";

const App = () => (
  <div className="app-shell">
    <h1>RAGHUVIR - Personal AI Assistant</h1>
    <Dashboard />
    <div className="grid">
      <ChatInterface />
      <PermissionManager />
      <MemoryViewer />
      <ActivityLog />
    </div>
  </div>
);

export default App;
