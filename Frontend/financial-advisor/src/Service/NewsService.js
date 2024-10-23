// NewsService.js
import axios from 'axios';

const NewsService = {
  getArticles: async () => {
    const response = await axios.get('http://127.0.0.1:8000/getarticles');
    return response.data;
  },
  getLatestArticles: async () => {
    const response = await axios.get('http://127.0.0.1:8000/getlatestarticles');  
    return response.data;
  },
  getEducationalResources: async () => {
    const response = await fetch('http://127.0.0.1:8000/educational_resources');
    if (!response.ok) throw new Error('Failed to fetch educational resources');
    return response.json();
  }
};

export default NewsService;