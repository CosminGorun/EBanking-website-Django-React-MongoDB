import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, useNavigate } from "react-router-dom";
import Login from './components/Login/login';
import SignUp from './components/SignUp/SignUp';
import EmailVerification from './components/ValidareMail/ValidareMail';
import './App.css';
import MainPage from './components/HomePage/mainPage';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const autentificat = localStorage.getItem('autentificat');
    
    if (autentificat) {
      setIsAuthenticated(true);
    } else {
      setIsAuthenticated(false);
    }
  }, []);

  useEffect(() => {
    if (!isAuthenticated) {
      navigate('/login');
    }
  }, [isAuthenticated, navigate]);

  return (
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/mainPage" element={<MainPage/>} />
        <Route path="/signUp" element={<SignUp/>}/> 
        <Route path="/mailVerification" element={<EmailVerification/>}/>
      </Routes>
  );
}

export default App;
