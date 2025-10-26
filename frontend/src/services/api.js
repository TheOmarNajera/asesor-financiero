import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://172.20.10.10:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para agregar X-Empresa-ID desde localStorage
api.interceptors.request.use(
  (config) => {
    const empresa_id = localStorage.getItem('empresa_id');
    if (empresa_id) {
      config.headers['X-Empresa-ID'] = empresa_id;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para manejar errores
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error);
    return Promise.reject(error);
  }
);

export default api;
