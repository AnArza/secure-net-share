import React from 'react';
import './Header.css';

const Header = ({ user, onLogout }) => {

  const handleLogout = async (event) => {
      event.preventDefault();
        try {
            const token = localStorage.getItem('token');
            const response = await fetch('/api/logout/', {
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (response.ok) {
                onLogout();
            } else {
                alert('Logout failed');
            }
        } catch (error) {
            alert('Logout error: ' + error.message)
        }
  }

  return (
      <header className="app-header">
          <h2>{user}'s Dashboard</h2>
          <button onClick={handleLogout} className="logout-button">Logout</button>
      </header>
  );
};

export default Header;
