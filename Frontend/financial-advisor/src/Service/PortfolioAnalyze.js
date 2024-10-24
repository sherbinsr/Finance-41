import axios from 'axios';

const API_URL = 'https://finance-41-1081098542602.us-central1.run.app/proxy/8000/analyze'; 

export const analyzePortfolio = async (portfolio) => {
    try {
        const response = await axios.post(API_URL, portfolio);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.error || 'Error analyzing portfolio');
    }
};
