import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/chat';

export const ChatService = async (message) => {
  try {
    const response = await axios.post(API_URL, { message });
    return response.data.response;
  } catch (error) {
    console.error('Error sending message to API:', error);
    return 'Sorry, I could not get a response from the server.';
  }
};
