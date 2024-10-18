// NewsService.js
import axios from 'axios';

const NewsService = {
  getArticles: async () => {
    const response = await axios.get('http://127.0.0.1:8000/getarticles');
    return response.data;
  },
  getLatestArticles: async () => {
    const response = await axios.get('http://127.0.0.1:8000/getlatestarticles');  // Latest articles API
    return response.data;
  }
};

export default NewsService;