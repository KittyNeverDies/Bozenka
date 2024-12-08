import { Box, Button, Input, Typography, Card, Grid } from '@mui/joy';
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import LinearProgress from '@mui/joy/LinearProgress';
import Alert from '@mui/joy/Alert';
import MailRoundedIcon from '@mui/icons-material/MailRounded';
import PersonRoundedIcon from '@mui/icons-material/PersonRounded';
import LockRoundedIcon from '@mui/icons-material/LockRounded';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
  });
  const [alert, setAlert] = useState({
    header: null,
    message: null,
    type: 'danger',
    useWaitAnimation: null,
    open: false,
  });


  const handleChange = (event) => {
    const { name, value } = event.target;
    setFormData((prevData) => ({ ...prevData, [name]: value }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    setAlert({ message: null, type: 'danger', open: false });

    const { email, password } = formData;

    if (!email || !password) {
      setAlert({
        message: 'Please fill in all fields of form to login',
        type: 'danger',
        useWaitAnimation: false,
        open: true,
      });
    } else {
      setAlert({
        message: 'Registration successful! Redirecting to dashboard...',
        type: 'success',
        useWaitAnimation: true,
        open: true,
      });
      setTimeout(() => {
        // Implement redirect logic here
      }, 2000);
    }
  };

  const handleCloseAlert = () => {
    setAlert((prevAlert) => ({ ...prevAlert, open: false }));
  };

  const inputStyles = {
    width: '100%',
    '--Input-focusedThickness': '1px',
    bgcolor: 'background.level0',
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
    {
      name: 'email',
      type: 'email',
      placeholder: 'Write your email',
      autoComplete: 'email',
      icon: <MailRoundedIcon />,
    },
    {
      name: 'password',
      type: 'password',
      placeholder: 'Write your password',
      autoComplete: 'password',
      icon: <LockRoundedIcon />,
    },
  ];

  return (
    <Box sx={{ maxWidth:1000, mx: 'auto', p: 4 }}>
      {alert.open && (
        <Box sx={{ textAlign: 'left', mb: 2 }}>
          <Alert
            color={alert.type}
            variant="solid"
            invertedColors
            sx={{ width: '100%' }}
            endDecorator={
            <Button
                variant="plain"
                color="neutral"
                onClick={handleCloseAlert}
                sx={{ p: 1.5 }}
              >
                <CloseRoundedIcon />
              </Button>}
          >
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
              <div sx={{ textAlign: 'left' }}>
                <Typography level="title-lg">{alert.type === 'success' ? 'Success' : 'Error'}</Typography>
                <Typography level="body-sm">{alert.message}</Typography>
              </div>
            </Box>
            
            {alert.useWaitAnimation && (
              <LinearProgress
                variant="solid"
                color={alert.type}
                size="sm"
                value={40}
                sx={{
                  position: 'absolute',
                  bottom: 0,
                  left: 0,
                  right: 0,
                  borderRadius: 0,
                }}
              />
            )}
          </Alert>
        </Box>
      )}
      <Card sx={{ p: 4, boxShadow: '0 2px 10px rgba(0, 0, 0, 0.08)' }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Typography variant="h2" level="h4" sx={{ fontWeight: 'bold', color: 'text.primary', fontSize: '1.75rem' }}>
              Login
            </Typography>
            <Typography level='body-sm'sx={{ mb: 3 }}>
              Login into account here, to work with unified community management.
            </Typography>
          </Grid>
          <Grid item xs={12} md={6} sx={{py: 3}}>
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
              <Typography level='body-xs'>Don't have an account? <Link to='/register/'>Register</Link></Typography>
              <Button
                variant="solid"
                type="submit"
                sx={{
                  mt: 2,
                  fontWeight: 'bold',
                  p: 1.5,
                  float: 'left',
                  transition: 'background-color 0.3s ease',
                }}
              >
                Login
              </Button>
            </form>
          </Grid>
        </Grid>
      </Card>
    </Box>
  );
};

export default LoginPage;