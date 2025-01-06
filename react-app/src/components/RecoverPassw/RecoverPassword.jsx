import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from '../axiosInstance';

const ForgotPassword = () => {
  const [username, setUserName] = useState('');
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleForgotPassword = async () => {
    try {
      const response = await axiosInstance.post('/forgotPassword', { username });
      console.log("Forgot password request sent successfully:", response.data);
      setError('');
      navigate('/mailVerificationPassw');
    } catch (err) {
      if (err.response && err.response.data && err.response.data.message) {
        setError(err.response.data.message);
      } else {
        setError("Username not found. Please try again.");
      }
    }
  };

  return (
    <div className="login-right">
      <div className="login-right-container">
        <div className="login-center">
          <h2>Forgot Password</h2>
          <p>Please enter your username to reset your password</p>
          <form>
            <input
              type="text"
              placeholder="User Name"
              value={username}
              onChange={(e) => setUserName(e.target.value)}
            />
            {error && <p className="error-message">{error}</p>}
            <div className="login-center-buttons">
              <button type="button" onClick={handleForgotPassword}>Submit</button>
            </div>
          </form>
        </div>

        <p className="login-bottom-p">
          Remember your password? <a href="#" onClick={() => navigate('/login')}>Log In</a>
        </p>
      </div>
    </div>
  );
};

export default ForgotPassword;