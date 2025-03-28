

import React, { createContext, useContext, useState, useCallback } from 'react';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [authState, setAuthState] = useState(() => ({
        accessToken: localStorage.getItem('accessToken'),
        refreshToken: localStorage.getItem('refreshToken'),
        isAuthenticated: !!localStorage.getItem('accessToken')
    }));


    const login = useCallback((accessToken, refreshToken) => {
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);
        setAuthState({
            accessToken,
            refreshToken,
            isAuthenticated: true
        });
    }, []);

    const logout = useCallback(() => {
        localStorage.removeItem('accessToken');
        localStorage.removeItem('refreshToken');
        setAuthState({
            accessToken: null,
            refreshToken: null,
            isAuthenticated: false
        });
    }, []);

    const updateTokens = useCallback((accessToken, refreshToken) => {
        localStorage.setItem('accessToken', accessToken);
        localStorage.setItem('refreshToken', refreshToken);
        setAuthState(prev => ({
            ...prev,
            accessToken,
            refreshToken
        }));
    }, []);

    return (
        <AuthContext.Provider value={{ ...authState, login, logout, updateTokens }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => {
    const context = useContext(AuthContext);
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider');
    }
    return context;
};

