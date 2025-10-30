import axios from 'axios';

const API_BASE_URL = 'http://localhost:5000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export const authAPI = {
  register: (userData) => api.post('/register', userData),
  login: (credentials) => api.post('/login', credentials),
};

export const medicineAPI = {
  getMedicines: (userId) => {
    if (!userId) {
      throw new Error('userId is required to fetch medicines');
    }
    return api.get('/medicines', { params: { user_id: userId } });
  },
  addMedicine: (medicineData) => api.post('/medicines', medicineData),
};

export const reminderAPI = {
  getReminders: (userId) => {
    if (!userId) {
      throw new Error('userId is required to fetch reminders');
    }
    return api.get('/reminders', { params: { user_id: userId } });
  },
};

export const prescriptionAPI = {
  uploadPrescription: (formData) => api.post('/upload-prescription', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  parseText: (data) => api.post('/parse-text', data),
};

export default api;