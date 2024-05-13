import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Home from './pages/Home';
import './App.css';

const App = () => {
    const [isLoggedIn, setIsLoggedIn] = useState(false);
    const [token, setToken] = useState(localStorage.getItem('token'));

    useEffect(() => {
        if (token) {
            setIsLoggedIn(true);
        } else {
            setIsLoggedIn(false);
        }
    }, [token]);


    const handleLogin = (data, username) => {
        localStorage.setItem('token', data.access);
        setToken(data.access);
    };


    const handleLogout = () => {
        localStorage.removeItem('token');
        setToken(null);
    };

    const handleRegister = (data) => {
        localStorage.setItem('token', data.access);
        setToken(data.access);
    };

    return (
        <Router>
            <Routes>
                <Route path="/login" element={!isLoggedIn ? <Login onLogin={handleLogin} /> : <Navigate to="/" />} />
                <Route path="/register" element={!isLoggedIn ? <Register onRegister={handleRegister} /> : <Navigate to="/" />} />
                <Route path="/" element={isLoggedIn ? <Home token={token} onLogout={handleLogout} /> : <Navigate to="/login" />} />
            </Routes>
        </Router>
    );
};

export default App;
