// src/Service/stockInfoService.js
import axios from 'axios';

export const fetchStockInfo = async (tickerId) => {
  const response = await axios.get(`http://127.0.0.1:8000/stock`, {
    params: { name: tickerId }, // Replace this with the correct API call based on your endpoint
  });
  return response.data;
};
