import React, { createContext, useState, useContext } from 'react';

const ai_application_url = process.env.REACT_APP_AI_APPLICATION_BASE_URL ? process.env.REACT_APP_AI_APPLICATION_BASE_URL : 'http://localhost:8000';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [accessToken, setAccessToken] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const login = async (credentials) => {
    setIsLoading(true);
    try {
      const response = await fetch(`{ai_application_url}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(credentials),
        credentials: 'include', // for cookies
      });

      const data = await response.json();
      setAccessToken(data.accessToken);
    } catch (error) {
      // Handle error
    } finally {
      setIsLoading(false);
    }
  };

  const logout = () => {
    setAccessToken(null);
    // Additional cleanup if needed
  };

  const refreshAccessToken = async () => {
    try {
      const response = await fetch('/api/refresh', {
        method: 'POST',
        credentials: 'include', // for cookies
      });
      const data = await response.json();
      setAccessToken(data.accessToken);
    } catch (error) {
      logout();
    }
  };

  return (
    <AuthContext.Provider 
      value={{ 
        accessToken, 
        isLoading, 
        login, 
        logout,
        refreshAccessToken 
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// Custom hook to use the auth context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
