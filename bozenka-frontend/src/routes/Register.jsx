
// Some stuff for React
import React, { useState, useMemo } from 'react';
import { Link } from 'react-router-dom';

// MUI joy Elements
import LinearProgress from '@mui/joy/LinearProgress';
import { Box, Button, Input, Typography, Card } from '@mui/joy';
import Alert from '@mui/joy/Alert';
import Step from '@mui/joy/Step';
import Stepper from '@mui/joy/Stepper';
import StepIndicator from '@mui/joy/StepIndicator';
import FormControl from '@mui/joy/FormControl';
import FormHelperText from '@mui/joy/FormHelperText';
import Fragment from 'react';
import Checkbox from '@mui/joy/Checkbox';
import Grid from '@mui/joy/Grid';

// Community API client
import CommunityApiClient from '../api/CommunityApiClient';


// Icons from MUI
import MailRoundedIcon from '@mui/icons-material/MailRounded';
import PersonRoundedIcon from '@mui/icons-material/PersonRounded';
import LockRoundedIcon from '@mui/icons-material/LockRounded';
import CloseRoundedIcon from '@mui/icons-material/CloseRounded';



/**
* RegisterPage component
* Component for the registration page of the application.
* @returns {JSX.Element} - The rendered registration page.
*/
function RegisterPage () {


    // Initialize API client
    const apiClient = useMemo(() => new CommunityApiClient(), []);
    
    const [formData, setFormData] = useState({
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
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

    
    const handleCloseAlert = () => {
      setAlert((prevAlert) => ({ ...prevAlert, open: false }));
    };

    const handleSubmit = async(event) => {
      event.preventDefault();
      setAlert({ message: null, type: 'danger' });

      const { username, email, password, confirmPassword } = formData;

      if (!username || !email || !password || !confirmPassword) {
        setAlert({ 
          message: 'Please fill in all fields of form to register', 
          type: 'danger',
          useWaitAnimation: false,
          open: true,
        });
      } else if (password !== confirmPassword) {
        setAlert({ 
          message: 'Passwords do not match', 
          type: 'danger',
          useWaitAnimation: false,
          open: true,
        });
      } else {
        
        try {
          // Show loading state
          setAlert({
            message: 'Logging in...',
            type: 'neutral',
            useWaitAnimation: true,
            open: true,
          });

          // Attempt login
          const response = await apiClient.register(username, email, password);

          if (response.success) {
            // Show success message
            setAlert({
              message: 'Registration successful! Redirecting to dashboard...',
              type: 'success',
              useWaitAnimation: true,
              open: true,
            });

            // Store tokens in localStorage
            localStorage.setItem('accessToken', response.access_token);
            localStorage.setItem('refreshToken', response.refresh_token);

            setTimeout(() => {
              window.location.href = '/dashboard';
            }, 2000);
          }
        } catch (error) {
          // Handle login error
          setAlert({
            message: 'Registration is failed. Something is failed.',
            type: 'danger',
            useWaitAnimation: false,
            open: true,
          });
          console.error('Login error:', error);
        }
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
      <Box sx={{ maxWidth:1000, mx: 'auto', p: 4}}>
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
                    <Typography level="title-lg">
                      {alert.type === 'success' ? 'Success' : 
                      alert.type === 'neutral' ? 'Info' : 'Error'}
                    </Typography>
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
        
        <Card sx={{ p: 4, backgroundColor: 'background.body', boxShadow: '0 2px 10px rgba(0, 0, 0, 0.08)' }}>
        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>

          <Typography variant="h2" level="h4" sx={{ fontWeight: 'bold', color: 'text.primary', fontSize: '1.75rem' }}>
            Registration
          </Typography>
          <Typography level='body-sm' sx={{ mb: 3, color: 'text.primary' }}>
            Create a new account here, to get started with unified community management.
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
            <FormControl size="sm" sx={{my: 1 }}>
                  <Checkbox
                      size='sm'
                      label={
                        <React.Fragment>
                          <Typography level='body-xs'>
                            I have read and agree to the{' '}
                            <Typography level='body-xs' sx={{ fontWeight: 'md' }}>
                              terms and conditions</Typography>.
                            </Typography>
                        </React.Fragment>
                      }
                  />
                    <FormHelperText>
                      <Typography level="body-xs">
                        Read our <Link href="#link">terms and conditions</Link>.
                      </Typography>
                    </FormHelperText>
                </FormControl>
            <Typography level='body-xs'>Already have an account? <Link to='/login/'>Login</Link></Typography>
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
              Register
            </Button>
          </form>
          </Grid>
          </Grid>
        </Card>
      </Box>
    );
};

export default RegisterPage;

