import axios from "axios";
import { API_HOST } from "./consts";

const api = axios.create({
  baseURL: API_HOST,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

api.interceptors.request.use(
  (config: any) => {
    const uuid = localStorage.getItem("uuid");
    if (uuid) {
      config.headers = {
        ...config.headers,
        "User-UUID": uuid,
      };
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response: any) => response,
  (error) => {
    // Only redirect to login for 401 errors if we're not already on the login page
    if (error.response?.status === 401 && !window.location.pathname.includes('/login')) {
      localStorage.removeItem("uuid");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default api;
