
// src/hooks/useApiState.js
import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export const useApiState = (initialState = null) => {
    const navigate = useNavigate();
    const { logout } = useAuth();
    const [data, setData] = useState(initialState);
    const [error, setError] = useState(null);
    const [isLoading, setIsLoading] = useState(false);

    const handleApiCall = useCallback(async (apiFunc, ...args) => {
        setIsLoading(true);
        setError(null);
        
        try {
            const result = await apiFunc(...args);
            setData(result);
            return result;
        } catch (err) {
            const errorMessage = err.message || 'An unexpected error occurred';
            
            switch (errorMessage) {
                case 'Session expired. Please login again.':
                    logout();
                    navigate('/login', { 
                        state: { message: 'Your session has expired. Please login again.' }
                    });
                    break;
                case 'Token expired':
                    // Token refresh is handled automatically by useApi hook
                    break;
                case 'Network Error':
                    setError('Unable to connect to the server. Please check your internet connection.');
                    break;
                case 'Rate limit exceeded':
                    setError('Too many requests. Please try again later.');
                    break;
                default:
                    setError(errorMessage);
            }
            
            throw err;
        } finally {
            setIsLoading(false);
        }
    }, [navigate, logout]);

    return {
        data,
        setData,
        error,
        setError,
        isLoading,
        setIsLoading,
        handleApiCall
    };
};
