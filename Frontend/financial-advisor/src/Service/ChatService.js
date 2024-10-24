import axios from 'axios';

const API_URL = 'https://finance-41-1081098542602.us-central1.run.app/proxy/8000/chat';

export const ChatService = async (message) => {
  try {
    const response = await axios.post(API_URL, { message });
    return response.data.response;
  } catch (error) {
    console.error('Error sending message to API:', error);
    return 'Sorry, I could not get a response from the server.';
  }
};
