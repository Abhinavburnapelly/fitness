import React from 'react';
import { Link } from 'react-router-dom'; // Import Link from react-router-dom
import './styles.css'; // Assuming you are using the same stylesheet
import '../App.css';

const MainPage = () => {
  return (
    <div className="main-page">
      <header>
        <nav>
          <div className="logo">
            <h1>FitnessHub</h1>
          </div>
          <ul>
            <li><a href="#about">About</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#contact">Contact</a></li>
          </ul>
        </nav>
      </header>
      <div className="buttons-container">
        {/* Use Link component to navigate to different routes */}
        <Link to="/livefeed/arm"> 
          <button className="main-page-button">Arms Exercise</button>
        </Link>
        <Link to="/livefeed/leg">
          <button className="main-page-button">Legs Exercise</button>
        </Link>
      </div>
    </div>
  );
};

export default MainPage;