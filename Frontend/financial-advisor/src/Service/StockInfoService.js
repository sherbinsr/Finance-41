
import axios from 'axios';

export const fetchStockInfo = async (tickerId) => {
  const response = await axios.get(`https://finance-41-1081098542602.us-central1.run.app/proxy/8000/stock`, {
    params: { name: tickerId }, 
    });
  return response.data;
};
