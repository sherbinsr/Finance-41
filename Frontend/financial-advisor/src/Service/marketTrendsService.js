import axios from 'axios';

const api_url = "http://127.0.0.1:8000/market-trends";

export const fetchMarketData = async () => {
  try {
    const response = await axios.get(api_url);
    return response.data.trending_stocks;
  } catch (err) {
    throw new Error(err.message);
  }
};
