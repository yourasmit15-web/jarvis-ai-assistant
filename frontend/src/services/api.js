import axios from "axios";

const client = axios.create({
  baseURL: process.env.REACT_APP_API_BASE_URL || "http://localhost:8000/api",
});

export const sendChatMessage = async (message) => (await client.post("/chat", { message })).data;
export const getStatus = async () => (await client.get("/status")).data;
export const emergencyStop = async (toggle = true) => (await client.post(`/stop?toggle=${toggle}`)).data;
export const getPermissions = async () => (await client.get("/permissions")).data;
export const updatePermissions = async (updates) => (await client.post("/permissions", { updates })).data;
export const addMemory = async (payload) => (await client.post("/memory", payload)).data;
export const getMemory = async (query) => (await client.get("/memory", { params: { query } })).data;
export const deleteMemory = async (id) => (await client.delete(`/memory/${id}`)).data;
export const getActivityLog = async () => (await client.get("/activity-log")).data;
