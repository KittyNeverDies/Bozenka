import { Box, Button, Input, Typography, Card } from '@mui/joy';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import Alert from '@mui/joy/Alert';


import MailRoundedIcon from '@mui/icons-material/MailRounded';
import PersonRoundedIcon from '@mui/icons-material/PersonRounded';
import LockRoundedIcon from '@mui/icons-material/LockRounded';

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
  });
  const [alert, setAlert] = useState({ message: null, type: 'danger' });

  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setAlert({ message: null, type: 'danger' });

    const { username, email, password, confirmPassword } = formData;

    if (!username || !email || !password || !confirmPassword) {
      setAlert({ message: 'Please fill in all fields', type: 'danger' });
    } else if (password !== confirmPassword) {
      setAlert({ message: 'Passwords do not match', type: 'danger' });
    } else {
      setAlert({ message: 'Registration successful! Redirecting to login page...', type: 'success' });
      setTimeout(() => {
        // Implement redirect logic here
      }, 2000);
    }
  };

  const inputStyles = {
    width: '100%',
    '--Input-focusedThickness': '1px',
    bgcolor: 'background.surface',
    borderRadius: 'lg',
    '&:hover': {
      bgcolor: 'background.level1',
      borderColor: 'primary.300',
    },
    '&:focus-within': {
      borderColor: 'background.level2',
      bgcolor: 'background.level1',
    },
    '&:focus': {
      outline: 'none',
    },
    mb: 2,
    py: 1.5,
    px: 2,
    fontSize: 'sm',
    fontWeight: 'md',
    border: '1px solid',
    borderColor: 'neutral.300',
    transition: 'box-shadow 0.2s ease-in-out, border-color 0.2s ease-in-out, background-color 0.2s ease-in-out',
    '&::placeholder': {
      color: 'neutral.500',
      fontStyle: 'italic',
    },
    '&:disabled': {
      bgcolor: 'neutral.100',
      color: 'neutral.400',
      cursor: 'not-allowed',
    },
  };

  const inputFields = [
    { name: 'email',  type: 'email', placeholder: 'Write your email', autoComplete: 'email', icon: <MailRoundedIcon/> },
    { name: 'username', type: 'text', placeholder: 'Enter your username', autoComplete: 'username', icon: <PersonRoundedIcon/> },
    { name: 'password', type: 'password', placeholder: 'Write your password', autoComplete: 'password', icon: <LockRoundedIcon/> },
    { name: 'confirmPassword',  type: 'password', placeholder: 'Confirm your password', autoComplete: 'new-password', icon: <LockRoundedIcon/> },
  ];

  return (
    <Box sx={{ maxWidth: 480, mx: 'auto', p: 4, mt: 4, mb: 15 }}>
      {alert.message && (
        <Box sx={{ textAlign: 'center', mb: 2 }}>
          <Alert color={alert.type} variant="soft" sx={{ width: '100%' }}>
            {alert.message}
          </Alert>
        </Box>
      )}
      <Card sx={{ p: 4, backgroundColor: '#fff', boxShadow: '0 2px 10px rgba(0, 0, 0, 0.08)' }}>
        <Typography variant="h2" level="h4" sx={{ fontWeight: 'bold', color: 'text.primary', fontSize: '1.75rem' }}>
          Registration
        </Typography>
        <Typography sx={{ mb: 3, color: 'text.primary' }}>
          Create a new account here, to get started with unified community management.
        </Typography>
        <form onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
          {inputFields.map((field) => (
            <Input
              key={field.name}
              name={field.name}
              type={field.type}
              placeholder={field.placeholder}
              value={formData[field.name]}
              onChange={handleChange}
              sx={inputStyles}
              startDecorator={field.icon}
              aria-label={`${field.name} input field`}
              autoComplete={field.autoComplete}
            />
          ))}
          <Button
            variant="solid"
            type="submit"
            sx={{
              width: '100%',
              mt: 2,
              backgroundColor: '#1976d2',
              color: '#fff',
              fontWeight: 'bold',
              p: 1.5,
              '&:hover': {
                backgroundColor: '#1565c0',
              },
              transition: 'background-color 0.3s ease',
            }}
          >
            Register
          </Button>
        </form>
        <Box sx={{ textAlign: 'center', mt: 3 }}>
          <Typography variant="body2" sx={{ color: '#666', mb: 1 }}>
            Already have an account?
          </Typography>
          <Button
            component={Link}
            to="/login"
            variant="outlined"
            sx={{
              width: '100%',
              borderColor: '#1976d2',
              color: '#1976d2',
              fontWeight: 'bold',
              p: 1.5,
              '&:hover': {
                backgroundColor: '#e3f2fd',
              },
              transition: 'background-color 0.3s ease',
            }}
          >
            Login
          </Button>
        </Box>
      </Card>
    </Box>
  );
};

export default RegisterPage;

