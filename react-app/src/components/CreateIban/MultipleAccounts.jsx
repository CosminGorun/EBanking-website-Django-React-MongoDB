import React, { useState, useEffect } from "react";
import axios from "axios";
import "./MultipleAccounts.css";

const MultipleAccounts = () => {
    const [accounts, setAccounts] = useState([]);
    const [error, setError] = useState("");

    useEffect(() => {
        const fetchAccounts = async () => {
            try {
                const response = await axios.get('/viewMultipleAccounts');
                setAccounts(response.data.accounts);
            } catch (err) {
                if (err.response && err.response.data) {
                    setError(err.response.data.message || "An error occurred.");
                } else {
                    setError("An error occurred. Please try again.");
                }
            }
        };

        fetchAccounts();
    }, []);
    return (
        <div className="accounts-container">
            <h1>Welcome to Multiple Accounts</h1>
            <p>This is a test page to check if routing works.</p>
            <ul>
                <li>Account 1: ABC123</li>
                <li>Account 2: DEF456</li>
                <li>Account 3: GHI789</li>
            </ul>
        </div>
    );
};

export default MultipleAccounts;