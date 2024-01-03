import React from 'react';
import ReactDOM from 'react-dom/client';
import './style.css';
import App from './App';


import { StyledEngineProvider } from '@mui/styled-engine';
import { BrowserRouter } from 'react-router-dom';


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <StyledEngineProvider injectFirst>
      <React.StrictMode>
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </React.StrictMode> 
  </StyledEngineProvider>
 
);
