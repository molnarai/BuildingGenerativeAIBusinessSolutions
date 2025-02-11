// LoginScreen.js
import React, { useState } from 'react';
// import { useNavigate } from 'react-router-dom';
import { useAuth } from '../AuthProvider';

const LoginScreen = ({ onLoginSuccess, ai_application_url }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  // const navigate = useNavigate();
  const { login, isLoading } = useAuth();


  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    const success = await login(username, password);
    if (success) {
      // navigate('');
    } else {
      setError('Invalid username or password');
    }
  };


  return (
    <div className="login-container">
      <form onSubmit={handleSubmit} className="login-form">
        <h2>Login</h2>
        {error && <div className="error-message">{error}</div>}
        <p>Use your ARC password to login in</p>
        <p> If you experience issues,
            try the <a href="http://www.insight.gsu.edu/z/" target="_blank">Password Reset Tool</a>
        </p>
        <div className="form-group">
          <label htmlFor="username">Username:</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Password:</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <button type="submit" disabled={isLoading}>
          {isLoading ? 'Logging in...' : 'Login'}
        </button>
      </form>
    </div>
  );
};

export default LoginScreen;
