import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axiosInstance from '../axiosInstance';

const ChangePassword = () => {
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  const navigate = useNavigate();

  const handleChangePassword = async () => {
    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      setSuccessMessage('');
      return;
    }

    try {
      const response = await axiosInstance.post('/changePassword', { newPassword });
      console.log("Password changed successfully:", response.data);
      setSuccessMessage("Your password has been changed successfully. Redirecting to login...");
      setError('');
      navigate('/login');
    } catch (err) {
      if (err.response && err.response.data && err.response.data.message) {
        setError(err.response.data.message);
      } else {
        setError("An error occurred. Please try again.");
      }
      setSuccessMessage('');
    }
  };

  return (
    <div className="login-right">
      <div className="login-right-container">
        <div className="login-center">
          <h2>Change Password</h2>
          <p>Please enter your new password</p>
          <form>
            <input
              type="password"
              placeholder="New Password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
            />
            <input
              type="password"
              placeholder="Confirm New Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
            />

            {error && <p className="error-message">{error}</p>}

            <div className="login-center-buttons">
              <button type="button" onClick={handleChangePassword}>Submit</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ChangePassword;
