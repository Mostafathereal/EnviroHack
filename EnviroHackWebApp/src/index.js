import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import LoginApp from './loginPage';
import GpsInput  from './gpsPage';

ReactDOM.render(
  <React.StrictMode>
    <GpsInput />
  </React.StrictMode>,
  document.getElementById('root')
);
