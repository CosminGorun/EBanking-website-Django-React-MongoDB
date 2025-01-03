import React, { useState, useEffect } from "react";
import axios from "axios";
import "./MultipleAccounts.css";
import axiosInstance from "../axiosInstance";
import {useNavigate} from "react-router-dom";

const MultipleAccounts = () => {
    const [accounts, setAccounts] = useState([]);
    const [error, setError] = useState("");
    const [currency, setCurrency] = useState("");
    const [userID, setUserID] = useState('');
     const navigate = useNavigate();
    // useEffect(() => {
    //     const fetchAccounts = async () => {
    //         try {
    //             const response = await axios.get('/viewMultipleAccounts');
    //             setAccounts(response.data.accounts);
    //         } catch (err) {
    //             if (err.response && err.response.data) {
    //                 setError(err.response.data.message || "An error occurred.");
    //             } else {
    //                 setError("An error occurred. Please try again.");
    //             }
    //         }
    //     };
    //     fetchAccounts();
    // }, []);
  const fetchUserID = async () => {
    axiosInstance.get('/mainPage')
      .then(response => {
        setUserID(response.data.USERID);
      })
      .catch(err => {
        setError('Error fetching transaction data');
        console.error(err);
      });
  };
    const handleCurrencyChange = (e) => {
        setCurrency(e.target.value);
    };

const handleFormSubmit = async (e) => {
    e.preventDefault();
    try {
        // POST userID and currency to the backend
        const response = await axios.post('/addAccount', { currency: currency, userID: userID });
        console.log(response.data.message);
        navigate('/mainPage');
    } catch (err) {
        if (err.response && err.response.data) {
            setError(err.response.data.message || "Failed to create account.");
        } else {
            setError("Failed to create account. Please try again.");
        }
    }
};

    return (
        <div className="accounts-container">
            <h2>Create a New Account</h2>
            <h3>Fill in the details below</h3>
            <form onSubmit={handleFormSubmit} className="accounts-form">
                <div className="form-group">
                    <label htmlFor="currencySelect">Select Currency:</label>
                    <select
                        id="currencySelect"
                        value={currency}
                        onChange={handleCurrencyChange}
                        required
                        className="form-control"
                    >
                        <option value="" disabled>
                            Select Currency
                        </option>
                        <option value="USD">USD (US Dollar)</option>
                        <option value="EUR">EUR (Euro)</option>
                        <option value="RON">RON (Romanian Leu)</option>
                        <option value="HUF">HUF (Hungarian Forint)</option>
                    </select>
                </div>
                <div className="form-actions">
                    <button type="submit" className="submit-button">
                        Create Account
                    </button>
                </div>
            </form>
        </div>
    );
};

export default MultipleAccounts;