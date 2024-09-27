import { Box, Button, Input, Typography, Card } from '@mui/joy';
import Alert from '@mui/joy/Alert';

import React, { useState } from 'react';
import { Link } from 'react-router-dom';

function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);

  const handleSubmit = (event) => {
    event.preventDefault();
    if (username === '' || password === '') {
      setError('Please fill in all fields');
    } else {
      // Api soon.
    }
  };

  return (
    <Box sx={{ 
        maxWidth: 400, 
        mx: 'auto', 
        p: 4, mt: 10, 
        marginBottom: 30, 
        textAlign: 'center' 
    }}>
      <Card sx={{
        [`& ${inputClasses}`]: {

        }
      }}>
        <Typography variant="h2" level='title-lg'>
          Login
        </Typography>
        <form onSubmit={handleSubmit}>
          <Input
            placeholder="Username"
            type="text"
            value={username}
            onChange={(event) => setUsername(event.target.value)}
            sx={{ mb: 2 }}
          />
          <Input
            placeholder="Password"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            sx={{ mb: 2 }}
          />
          <Button variant="solid" type="submit">
            Login
          </Button>
          
          {error && (

            <Alert color='danger' variant='soft' sx={{mt: 1, textAlign: 'center'}}>{error}</Alert>
          )}
        </form>
        <Box sx={{ textAlign: 'left', mt: 2 }}>
          <Button component={Link} to="/register" variant="outlined">
            Register
          </Button>
        </Box>
      </Card>
    </Box>
  );
}

export default LoginPage;
