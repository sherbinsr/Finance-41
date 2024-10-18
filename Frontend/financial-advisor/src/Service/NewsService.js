// src/NewsService.js
import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/getarticles';

class NewsService {
  static async getArticles() {
    try {
      const response = await axios.get(API_URL);
      return response.data; // Return the data from the API response
    } catch (error) {
      console.error('Error fetching articles:', error);
      throw error; // Propagate error so it can be handled in the component
    }
  }
}

export default NewsService;
