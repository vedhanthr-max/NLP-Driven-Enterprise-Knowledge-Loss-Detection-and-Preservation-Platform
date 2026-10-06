import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Request interceptor to attach bearer token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
}, (error) => Promise.reject(error));

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      // If token expired or unauthorized and not on login page
      if (!window.location.pathname.includes('/login')) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user_info');
      }
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  login: (email, password) => api.post('/auth/login', { email, password }),
  register: (data) => api.post('/auth/register', data),
  getMe: () => api.get('/auth/me'),
  logout: () => api.post('/auth/logout'),
};

export const documentAPI = {
  upload: (formData) => api.post('/documents/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  getAll: (page = 1, limit = 20) => api.get(`/documents?page=${page}&limit=${limit}`),
  getDetails: (id) => api.get(`/documents/${id}`),
  delete: (id) => api.delete(`/documents/${id}`),
};

export const knowledgeAPI = {
  getAll: (params = {}) => api.get('/knowledge', { params }),
  getDetails: (id) => api.get(`/knowledge/${id}`),
  create: (data) => api.post('/knowledge', data),
  update: (id, data) => api.put(`/knowledge/${id}`, data),
};

export const riskAPI = {
  getDashboard: () => api.get('/risk/dashboard'),
  analyze: (id, data) => api.post(`/risk/analyze/${id}`, data),
  simulate: (factors) => api.post('/risk/simulate', factors),
  getHistory: (id) => api.get(`/risk/history/${id}`),
};

export const mlAPI = {
  getMetrics: () => api.get('/ml/metrics'),
  predict: (data) => api.post('/ml/predict', data),
  train: () => api.post('/ml/train'),
};

export const searchAPI = {
  semanticSearch: (q, limit = 10) => api.get(`/search?q=${encodeURIComponent(q)}&limit=${limit}`),
};

export const preservationAPI = {
  getAll: (params = {}) => api.get('/preservation-actions', { params }),
  create: (data) => api.post('/preservation-actions', data),
  update: (id, data) => api.put(`/preservation-actions/${id}`, data),
};

export const employeeAPI = {
  getAll: () => api.get('/employees'),
};

export const auditAPI = {
  getLogs: (limit = 50, action_type = null) => {
    let url = `/audit/logs?limit=${limit}`;
    if (action_type) url += `&action_type=${action_type}`;
    return api.get(url);
  },
};

export default api;
