import axios from "axios";

const baseURL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use((config) => {
  console.log("➡️ Request:", config.baseURL + config.url);
  return config;
});

api.interceptors.response.use(
  (response) => {
    console.log("✅ Response:", response);
    return response;
  },
  (error) => {
    console.log("❌ Axios Error:", error);
    throw error;
  }
);

export async function apiGet(url, config) {
  const res = await api.get(url, config);
  return res.data;
}

export async function apiPost(url, data, config) {
  const res = await api.post(url, data, config);
  return res.data;
}

export async function apiPut(url, data, config) {
  const res = await api.put(url, data, config);
  return res.data;
}