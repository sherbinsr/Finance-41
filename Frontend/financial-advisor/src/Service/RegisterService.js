// src/services/registerService.js
import axios from "axios";

const registerUser = async (username, email, password) => {
  try {
    const response = await axios.post("http://127.0.0.1:8000/register", {
      username,
      email,
      password,
    });
    return response.data; // Assuming the response has relevant data
  } catch (error) {
    throw error.response?.data?.detail || "User already Exists Registration failed!";
  }
};

export default registerUser;
