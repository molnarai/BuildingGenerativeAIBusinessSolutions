// LoginStatusWidget.js
import React from 'react';
// import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthProvider';
import './LoginStatusWidget.css';

// const LoginStatusWidget = ({ userInfo, onLogout, ai_application_url }) => {
const LoginStatusWidget = ({  }) => {
  // const navigate = useNavigate();
  const { user, logout } = useAuth();

  // const handleLogout = async () => {
  //   try {
  //     const response = await fetch(`${ai_application_url}/auth/logout`, {
  //       method: 'POST',
  //       headers: {
  //         'Authorization': `Bearer ${localStorage.getItem('authToken')}`,
  //       },
  //     });

  //     if (!response.ok) {
  //       throw new Error('Logout failed');
  //     }

  //     localStorage.removeItem('authToken');
  //     localStorage.removeItem('username');
  //     onLogout();
  //   } catch (error) {
  //     console.error('Logout error:', error);
  //   }
  // };

  const handleLogout = async () => {
    await logout();
    // navigate('login');
  };

  const handleLoginClick = () => {
    // navigate('login');
  };

  return (
    <div className="login-status-widget">
      {user?.is_authenticated ? (
        <div className="user-info">
          <div className="user-details">
            <span className="welcome-text">
              Welcome, {user.full_name || user.username || user.email || 'Guest'}
            </span>
            {user.is_admin && (
              <span className="admin-badge">Admin</span>
            )}
          </div>
          <button 
            className="logout-button"
            onClick={handleLogout}
          >
            Logout
          </button>
        </div>
      ) : (
        <div className="login-prompt">
          <span>Not logged in</span>
        </div>
      )}
    </div>
  );
};

export default LoginStatusWidget;
