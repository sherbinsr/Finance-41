import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom"; // Import useNavigate
import registerUser from "../Service/RegisterService"; // Import the service

const Register = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const [alertType, setAlertType] = useState(""); // Success or Error alert

  const navigate = useNavigate(); // Initialize useNavigate

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      await registerUser(username, email, password); // Use the service

      setMessage("Registration successful!");
      setAlertType("success");
      navigate('/login'); 
      setUsername("");
      setEmail("");
      setPassword("");
    } catch (error) {
    
      setMessage(error);
      setAlertType("danger");
    }
  };

  return (
    <div className="d-flex justify-content-center align-items-center vh-100">
      <div className="card shadow p-4" style={{ maxWidth: "400px", width: "100%" }}>
        <h2 className="text-center mb-4">Register</h2>
        
        {/* Alert message */}
        {message && (
          <div className={`alert alert-${alertType} text-center`} role="alert">
            {message}
          </div>
        )}

        <form onSubmit={handleRegister}>
          <div className="mb-3">
            <label htmlFor="username" className="form-label">
              Username
            </label>
            <input
              type="text"
              className="form-control"
              id="username"
              placeholder="Enter your username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="email" className="form-label">
              Email
            </label>
            <input
              type="email"
              className="form-control"
              id="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>
          <div className="mb-3">
            <label htmlFor="password" className="form-label">
              Password
            </label>
            <input
              type="password"
              className="form-control"
              id="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>
          <button type="submit" className="btn btn-primary w-100">
            Register
          </button>
        </form>
        <p className="text-center mt-3">
          Already registered? <Link to="/login">Login</Link>
        </p>
      </div>
    </div>
  );
};

export default Register;
