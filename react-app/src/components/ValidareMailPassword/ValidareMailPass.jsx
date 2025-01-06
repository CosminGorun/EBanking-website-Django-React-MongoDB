import React, { useState } from 'react';
import axios from 'axios';
import '../ValidareMail/EmVerification.css';
import { useNavigate } from "react-router-dom";

const EmailVerificationPassw = ({ mail }) => {
  const [codVerificare, setcodVerificare] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
        const response = await axios.post('/mailVerificationPass', { codVerificare: codVerificare });
        setSuccess('Verification successful!');
        setError('');
        localStorage.setItem('autentificat', 1);
        navigate('/changePassword');
    } 
     catch (error) {
      setError('The code is incorrect. Please try again.');
    }
  };

  return (
    <div className="container">
      <h2>Email Verification</h2>
      <p>An email has been sent to: <strong>{mail}</strong> </p>
      <p> Please enter the verification code below:</p>

      <form onSubmit={handleSubmit}>
        <label htmlFor="code">Verification Code:</label>
        <input
          type="text"
          id="code"
          name="codVerificare"
          value={codVerificare}
          onChange={(e) => setcodVerificare(e.target.value)}
          placeholder="Enter code here"
          required
        />
        
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
        
        <button type="submit">Verify</button>
      </form>
    </div>
  );
};

export default EmailVerificationPassw;
