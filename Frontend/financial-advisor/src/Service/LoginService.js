import axios from 'axios';

const API_URL = 'https://finance-41-1081098542602.us-central1.run.app/proxy/8000'; 

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
