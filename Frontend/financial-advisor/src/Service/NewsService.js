// NewsService.js
import axios from 'axios';

const NewsService = {
  getArticles: async () => {
    const response = await axios.get('https://finance-41-1081098542602.us-central1.run.app/proxy/8000/getarticles');
    return response.data;
  },
  getLatestArticles: async () => {
    const response = await axios.get('https://finance-41-1081098542602.us-central1.run.app/proxy/8000/getlatestarticles');  
    return response.data;
  },
  getEducationalResources: async () => {
    const response = await fetch('https://finance-41-1081098542602.us-central1.run.app/proxy/8000/educational_resources');
    if (!response.ok) throw new Error('Failed to fetch educational resources');
    return response.json();
  }
};

export default NewsService;