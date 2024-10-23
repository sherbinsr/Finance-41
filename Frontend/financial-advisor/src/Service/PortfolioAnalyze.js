import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/analyze'; 

export const analyzePortfolio = async (portfolio) => {
    try {
        const response = await axios.post(API_URL, portfolio);
        return response.data;
    } catch (error) {
        throw new Error(error.response?.data?.error || 'Error analyzing portfolio');
    }
};
