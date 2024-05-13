import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import './AuthForm.css';

const Login = ({ onLogin }) => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await fetch('/api/login/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ username, password })
            });

            if (response.ok) {
                const data = await response.json();
                onLogin(data, username);
            } else {
                alert('Login failed');
            }
        } catch (error) {
            alert('Login error: ' + error.message)
        }
    };

    return (
        <div className="auth-page">
            <div className="auth-container">
                <div>
                    <h2>Welcome to SecureNetShare</h2>
                    <form onSubmit={handleSubmit} className="auth-form">
                        <input
                            type="text"
                            placeholder="Username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            className="auth-input"
                        />
                        <input
                            type="password"
                            placeholder="Password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            className="auth-input"
                        />
                        <button type="submit" className="auth-button">Log In</button>
                    </form>
                    <div className="auth-switch">
                        <p>Don't have an account? <Link to="/register" className="auth-link">Register now</Link></p>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default Login;
