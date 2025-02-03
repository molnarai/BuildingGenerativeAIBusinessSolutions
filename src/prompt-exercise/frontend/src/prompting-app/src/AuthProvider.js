import React, { createContext, useState, useContext, useEffect } from 'react';

//const ai_application_url = process.env.REACT_APP_AI_APPLICATION_BASE_URL ? process.env.REACT_APP_AI_APPLICATION_BASE_URL : 'http://localhost:8000';

const AuthContext = createContext(null);

export const AuthProvider = ({ children, ai_application_url }) => {
    const [accessToken, setAccessToken] = useState(null);
    const [refreshToken, setRefreshToken] = useState(null);
    const [user, setUser] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [isAuthenticated, setIsAuthenticated] = useState(false);

    // Initialize auth state from localStorage
    useEffect(() => {
        const initializeAuth = async () => {
        const storedAccessToken = localStorage.getItem('accessToken');
        const storedUser = localStorage.getItem('user');

        if (storedAccessToken && storedUser) {
            try {
            // Verify token is still valid with the backend
            const response = await fetch(`${ai_application_url}/auth/verify`, {
                headers: {
                'Authorization': `Bearer ${storedAccessToken}`
                }
            });

            if (response.ok) {
                setAccessToken(storedAccessToken);
                setUser(JSON.parse(storedUser));
            } else {
                // Token is invalid, try to refresh
                await refreshAccessToken();
            }
            } catch (error) {
            console.error('Auth initialization error:', error);
            // Clear stored auth data if verification fails
            localStorage.removeItem('accessToken');
            localStorage.removeItem('refreshToken');
            localStorage.removeItem('user');
            }
        }
        setIsLoading(false);
        };

        initializeAuth();
    }, [ai_application_url]);


    const login = async (username, password) => {
        setIsLoading(true);
        try {
            const response = await fetch(`${ai_application_url}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password
                }),
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Login failed');
            }

            // Store tokens and update user state
            setAccessToken(data.access_token);
            localStorage.setItem('refreshToken', data.refresh_token);
            localStorage.setItem('authToken', data.refresh_token);
            localStorage.setItem('username', data.user.username);
            setUser({
                user_id: data.user.user_id,
                username: data.user.username,
                email: data.user.email,
                is_authenticated: true,
                auth_token: data.access_token
            });
            setIsAuthenticated(true);
            return true; // Return true for successful login
        } catch (error) {
            console.error('Login error:', error);
            setIsAuthenticated(false);
            return false; // Return false for failed login
        } finally {
            setIsLoading(false);
        }
    };

    const logout = () => {
        setAccessToken(null);
        setRefreshToken(null);
        setIsAuthenticated(false);
        localStorage.removeItem('refreshToken');
        setUser(null);
        setIsLoading(false);
        // clear localStorages
        localStorage.removeItem('username');
        
        // remove all items from localStorage
        // localStorage.clear();
        // Additional cleanup if needed
    };

    const refreshAccessToken = async () => {
        try {
            const response = await fetch(`${ai_application_url}/auth/refresh`, {
                method: 'POST',
                credentials: 'include', // for cookies
            });
            const data = await response.json();
            // setAccessToken(data.accessToken);
            setAccessToken(data.access_token);
        } catch (error) {
            logout();
        }
    };

    return (
        <AuthContext.Provider
            value={{
                accessToken,
                refreshToken,
                isLoading,
                isAuthenticated,
                user,
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
