// src/Service/AuthService.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000'; 

export const AuthService = {
  
  login: async (userData) => {
    try {
      const response = await axios.post(`${API_URL}/login`, userData);
      return response.data;
    } catch (error) {
      throw error.response.data.detail || 'Login failed';
    }
  },
};
