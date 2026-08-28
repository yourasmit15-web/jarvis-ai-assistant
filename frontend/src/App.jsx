import React from "react";
import ChatInterface from "./components/ChatInterface";
import Dashboard from "./components/Dashboard";
import PermissionManager from "./components/PermissionManager";
import MemoryViewer from "./components/MemoryViewer";
import ActivityLog from "./components/ActivityLog";

export default function App() {
  return (
    <main className="app-shell">
      <h1>JARVIS - Phase 1</h1>
      <Dashboard />
      <section className="grid">
        <ChatInterface />
        <PermissionManager />
        <MemoryViewer />
        <ActivityLog />
      </section>
    </main>
  );
}
