import React from 'react';
import ReactDOM from 'react-dom/client';
import {TTSForm} from './App';
import reportWebVitals from './reportWebVitals';
import 'uikit/dist/css/uikit.min.css';
import 'uikit/dist/js/uikit.min.js';
import 'uikit/dist/js/uikit-icons.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.min.js';
import './fonts.css'
import './styles.css'

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <TTSForm />
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
