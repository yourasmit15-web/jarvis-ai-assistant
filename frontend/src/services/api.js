import axios from "axios";

const api = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:8000",
});

export const sendChat = (message) => api.post("/api/chat", { message });
export const getStatus = () => api.get("/api/status");
export const getPermissions = () => api.get("/api/permissions");
export const updatePermission = (permission, enabled) =>
  api.post("/api/permissions", { permission, enabled });
export const getMemory = () => api.get("/api/memory");
export const addMemory = (category, content) => api.post("/api/memory", { category, content });
export const deleteMemory = (id) => api.delete(`/api/memory/${id}`);
export const getActivityLog = () => api.get("/api/activity-log");
export const emergencyStop = () => api.post("/api/stop");
