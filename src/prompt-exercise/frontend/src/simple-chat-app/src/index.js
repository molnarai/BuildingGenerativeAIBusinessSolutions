/*
 * Copyright (c) 2025 Péter Molnár
 * LinkedIn: https://www.linkedin.com/in/petermolnar/
 *
 * This code is licensed under the Creative Commons license. 
 * You are free to use, modify, and distribute it as long as proper attribution is provided.
 * 
 * Authorship: Péter Molnár with assistance from AI tools.
 * 
 * Disclaimer: This code is provided "as is", without any guarantees of correctness or functionality.
 * Use it at your own risk. The author assumes no liability for any issues arising from its use.
 * 
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
