import axios from "axios";

import { API_URL } from "@/lib/constants";
import { getStoredSession, setStoredSession } from "@/lib/sessionMetadata";
import { clearConversationDB } from "@/lib/conversation_db";

const api = axios.create({
  baseURL: API_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
  withCredentials: true,
});

api.interceptors.request.use(
  async (config) => {
    try {
      const session = await getStoredSession();
      if (session) {
        config.headers["X-Session-ID"] = session;
      }
    } catch (err) {
      console.error("Error reading stored session:", err);
    }
    return config;
  },
  (error) => Promise.reject(error),
);

api.interceptors.response.use(
  async (response) => {
    const session = response.headers["x-session-id"] || response.headers["X-Session-ID"];
    if (!session) {
      return response;
    }

    const current = await getStoredSession();
    if (current && current !== session) {
      await clearConversationDB();
    }
    await setStoredSession(session);
    return response;
  },

  (error) => Promise.reject(error),
);

export default api;

