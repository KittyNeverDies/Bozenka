
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useApi } from '../hooks/useApi';


export const useAuthForm = (formType = 'login') => {
    const navigate = useNavigate();
    const { login, checkAuthState } = useAuth();
    const api = useApi();
    
    const [formData, setFormData] = useState({
        username: '',
        email: formType === 'register' ? '' : undefined,
        password: '',
        confirmPassword: formType === 'register' ? '' : undefined,
        acceptTerms: formType === 'register' ? false : undefined
    });

    const [alert, setAlert] = useState({
        message: null,
        type: 'danger',
        useWaitAnimation: false,
        open: false
    });

    const handleChange = (event) => {
        const { name, value, checked } = event.target;
        setFormData(prev => ({
            ...prev,
            [name]: name === 'acceptTerms' ? checked : value
        }));
    };

    const validateForm = () => {
        if (formType === 'login') {
            if (!formData.username || !formData.password) {
                setAlert({
                    message: 'Please fill in all fields',
                    type: 'danger',
                    useWaitAnimation: false,
                    open: true
                });
                return false;
            }
        } else {
            if (!formData.username || !formData.email || !formData.password || !formData.confirmPassword) {
                setAlert({
                    message: 'Please fill in all fields',
                    type: 'danger',
                    useWaitAnimation: false,
                    open: true
                });
                return false;
            }
            if (formData.password !== formData.confirmPassword) {
                setAlert({
                    message: 'Passwords do not match',
                    type: 'danger',
                    useWaitAnimation: false,
                    open: true
                });
                return false;
            }
            if (!formData.acceptTerms) {
                setAlert({
                    message: 'Please accept the terms and conditions',
                    type: 'danger',
                    useWaitAnimation: false,
                    open: true
                });
                return false;
            }
        }
        return true;
    };

    const handleSubmit = async (event) => {
        event.preventDefault();
        setAlert({ message: null, type: 'danger', open: false });

        if (!validateForm()) return;

        try {
            setAlert({
                message: formType === 'login' ? 'Logging in...' : 'Creating account...',
                type: 'neutral',
                useWaitAnimation: true,
                open: true
            });

            const response = formType === 'login' 
                ? await api.login(formData.username, formData.password)
                : await api.register(formData.username, formData.email, formData.password);

            if (response.success) {
                // Use AuthContext login function to securely store tokens
                login(response.access_token, response.refresh_token);
                
                console.error(login)

                setAlert({
                    message: `${formType === 'login' ? 'Login' : 'Registration'} successful! Redirecting...`,
                    type: 'success',
                    useWaitAnimation: true,
                    open: true
                });

                // Use React Router navigation
                setTimeout(() => {
                    navigate('/dashboard');
                }, 2000);
            }
        } catch (error) {
            setAlert({
                message: `${formType === 'login' ? 'Login' : 'Registration'} failed. Please try again.`,
                type: 'danger',
                useWaitAnimation: false,
                open: true
            });
            console.error(`${formType} error:`, error);
        }
    };

    const handleCloseAlert = () => {
        setAlert(prev => ({ ...prev, open: false }));
    };

    return {
        formData,
        alert,
        handleChange,
        handleSubmit,
        handleCloseAlert
    };
};
