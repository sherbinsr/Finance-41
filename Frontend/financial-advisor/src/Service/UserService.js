import axios from 'axios';

class UserService {
  static async getUserCount() {
    try {
      const response = await axios.get('http://127.0.0.1:8000/user-count');
      return response.data.user_count;
    } catch (error) {
      console.error('Error fetching user count:', error);
      throw error;
    }
  }
}

export default UserService;
