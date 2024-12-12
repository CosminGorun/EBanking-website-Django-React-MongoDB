import React, { useState } from "react";
import { FaEye, FaEyeSlash } from "react-icons/fa6";
import axios from "axios";
import validator from "validator";
import { useNavigate } from "react-router-dom";
import "./SignUp.css"

const SignUp = () => {
    const [showPassword, setShowPassword] = useState(false);
    const [name, setName] = useState('');
    const [age, setAge] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [mail, setMail] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [errors, setErrors] = useState({});
    const navigate = useNavigate();

    const handleCreateAccount = async () => {
        
        let validationErrors = {};

        if (name.length < 3) {
            validationErrors.name = "Numele este prea scurt!";
        } else if (/[{}\[\],._;:\|!@#$%^&*()-_=+|~<>?]/.test(name)) {
            validationErrors.name = "Numele nu poate contine caractere speciale!";
        }

        if (!age || isNaN(age) || age < 18) {
            validationErrors.age = "Varsta trebuie sa fie mai mare de 18 ani!";
        }

        if (username.length < 5) {
            validationErrors.username = "Username-ul este prea scurt!";
        }

        if (password.length < 8) {
            validationErrors.password = "Parola trebuie sa contina minim 8 caractere!";
        }

        if (!validator.isEmail(mail)) {
            validationErrors.mail = "Email invalid!";
        }

        if (phoneNumber.length !== 10 || !/^\d+$/.test(phoneNumber)) {
            validationErrors.phoneNumber = "Numar gresit!";
        }

        setErrors(validationErrors);

        if (Object.keys(validationErrors).length === 0) {
            try {
            const response = await axios.post('/createAccount', {
                name,
                age,
                username,
                password,
                mail,
                phoneNumber
            });
            navigate('/mailVerification');
            } catch (err) {
            if (err.response && err.response.data) {
                setErrors(err.response.data.errors || {});
            } else {
                setErrors({ global: "An error occurred. Please try again." });
                }
            }
        }
      };
    

  return (
    <div className="login-main">
      <div className="login-right">
        <div className="form-page">
          <div>
            <h2>Create an account</h2>
            <h3>Please enter your details</h3>
            <form>
              {errors.name && <p className="error-message">{errors.name}</p>}
              <input
                type="text"
                placeholder="Name"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />

              {errors.age && <p className="error-message">{errors.age}</p>}
              <input
                type="text"
                placeholder="Age"
                value={age}
                onChange={(e) => setAge(e.target.value)}
              />

              {errors.username && <p className="error-message">{errors.username}</p>}
              <input
                type="text"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
              />
              
              {errors.mail && <p className="error-message">{errors.mail}</p>}
              <input
                type="email"
                placeholder="Email"
                value={mail}
                onChange={(e) => setMail(e.target.value)}
              />
              
              {errors.password && <p className="error-message">{errors.password}</p>}
              <div className="pass-input-div">
                <input
                  type={showPassword ? "text" : "password"}
                  placeholder="Password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
                {showPassword ? (
                  <FaEyeSlash onClick={() => setShowPassword(!showPassword)} />
                ) : (
                  <FaEye onClick={() => setShowPassword(!showPassword)} />
                )}
              </div>

              {errors.phoneNumber && <p className="error-message">{errors.phoneNumber}</p>}
              <input
                type="text"
                placeholder="Phone Number"
                value={phoneNumber}
                onChange={(e) => setPhoneNumber(e.target.value)}
              />

              {errors.global && <p className="error-message">{errors.global}</p>}

              <div className="login-center-buttons">
                <button type="button" onClick={handleCreateAccount}>Create Account</button>
              </div>
            </form>
          </div>

          <p className="login-bottom-p">
            Already have an account? <a href="#" onClick={() => navigate('/login')}>Sign in</a>
          </p>
        </div>
      </div>
    </div>
  );
};

export default SignUp;
