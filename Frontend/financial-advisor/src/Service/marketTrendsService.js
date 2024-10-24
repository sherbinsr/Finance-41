import axios from 'axios';

const api_url = "https://finance-41-1081098542602.us-central1.run.app/proxy/8000/market-trends";

export const fetchMarketData = async () => {
  try {
    const response = await axios.get(api_url);
    return response.data.trending_stocks;
  } catch (err) {
    throw new Error(err.message);
  }
};
