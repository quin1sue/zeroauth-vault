import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000', // Your FastAPI URL
});

// The "Interceptor" - The automated robot that adds your JWT
api.interceptors.request.use((config) => {
  // Grab the "Ticket" from the browser's storage
  const token = typeof window !== 'undefined' ? localStorage.getItem('bondee_token') : null;

  if (token) {
    // Add the "Bearer" header
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, error => {
    return Promise.reject(error)
});

export default api;