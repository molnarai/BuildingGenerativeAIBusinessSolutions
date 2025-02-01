// LoginStatusWidget.js
import React from 'react';
import { useNavigate } from 'react-router-dom';

const LoginStatusWidget = ({ userInfo, onLogout, ai_application_url }) => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const response = await fetch(`${ai_application_url}/auth/logout`, {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
        },
      });

      if (!response.ok) {
        throw new Error('Logout failed');
      }

      localStorage.removeItem('authToken');
      localStorage.removeItem('username');
      onLogout();
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  const handleLoginClick = () => {
    navigate('/login');
  };

  return (
    <div className="login-status-widget">
      {userInfo.username ? (
        <div className="user-info">
          <span>Welcome, {userInfo.username}</span>
          <button onClick={handleLogout}>Logout</button>
        </div>
      ) : (
        <button onClick={handleLoginClick}>Login</button>
      )}
    </div>
  );
};

export default LoginStatusWidget;
