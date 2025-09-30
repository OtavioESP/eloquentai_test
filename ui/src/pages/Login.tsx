import "./Login.css";
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { makeLogin, unloggedEntry } from "../services/services";
import { toast } from "react-toastify";


const Login = () => {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      const data = await makeLogin(username, password);
      console.log("Login successful:", data);
      const userUUID = data.user.id;
      navigate(`/chat/${userUUID}`, { replace: true });

    } catch (err: any) {
      console.error("Login error:", err);
      
      // Handle different types of errors
      if (err.response?.status === 401) {
        toast.error("Invalid username or password. Please try again.");
      } else if (err.response?.status === 400) {
        toast.error("Please check your input and try again.");
      } else if (err.code === 'ECONNABORTED') {
        toast.error("Request timed out. Please try again.");
      } else if (!err.response) {
        toast.error("Network error. Please check your connection and try again.");
      } else {
        toast.error("Login failed. Please try again.");
      }
    }
  };

  const withoutLogin = async () => {
    try {
      const data = await unloggedEntry();
      console.log("Unlogged entry successful:", data);
      const userUUID = data.user.id;
      navigate(`/chat/${userUUID}`, { replace: true });

    } catch (err: any) {
      console.error("Unlogged entry error:", err);
      
      // Handle different types of errors
      if (err.response?.status === 401) {
        toast.error("Unable to continue without login. Please try logging in.");
      } else if (err.response?.status === 400) {
        toast.error("Invalid request. Please try again.");
      } else if (err.code === 'ECONNABORTED') {
        toast.error("Request timed out. Please try again.");
      } else if (!err.response) {
        toast.error("Network error. Please check your connection and try again.");
      } else {
        toast.error("Unable to continue without login. Please try again.");
      }
    }
  }

  return (
    <div className="login-body">
      <div className="login-container">
        <div className="login-card">
          <h1 className="login-title">RAG chat</h1>
          <form onSubmit={handleSubmit} className="login-form">
            <label htmlFor="username">username</label>
            <input
              id="username"
              type="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Enter your username"
            />

            <label htmlFor="password">Password</label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter your password"
            />

            <button type="submit" className="login-button">
              Log In
            </button>

            <button 
              type="button" 
              className="unlogged-button" 
              onClick={withoutLogin}
            >
              Continue without login
            </button>

          </form>
        </div>
      </div>
    </div>
  );
};

export default Login;
