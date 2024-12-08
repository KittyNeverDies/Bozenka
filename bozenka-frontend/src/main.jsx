import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { StyledEngineProvider } from '@mui/joy/styles';
import { CssVarsProvider } from '@mui/joy/styles';
import softTheme from './theme';

import App from './App.jsx'
import './index.css'
import { BrowserRouter } from 'react-router-dom';


createRoot(document.getElementById('root')).render(
  <BrowserRouter>
  <CssVarsProvider defaultMode="system" theme={softTheme}>  
    <StrictMode>
        <StyledEngineProvider injectFirst>
          <App />
        </StyledEngineProvider>
    </StrictMode>
  </CssVarsProvider>
  </BrowserRouter>
)
