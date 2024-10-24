import axios from 'axios';

class UserService {
  static async getUserCount() {
    try {
      const response = await axios.get('https://finance-41-1081098542602.us-central1.run.app/proxy/8000/user-count');
      return response.data.user_count;
    } catch (error) {
      console.error('Error fetching user count:', error);
      throw error;
    }
  }
}

export default UserService;
