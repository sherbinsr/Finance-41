
import axios from "axios";

const registerUser = async (username, email, password) => {
  try {
    const response = await axios.post("https://finance-41-1081098542602.us-central1.run.app/proxy/8000/register", {
      username,
      email,
      password,
    });
    return response.data; 
  } catch (error) {
    throw error.response?.data?.detail || "User already Exists Registration failed!";
  }
};

export default registerUser;
