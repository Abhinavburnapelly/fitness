import React, { useState, useEffect } from 'react';
import './App.css'
import LiveFeed from './components/LiveFeed';
import Chatbot from './components/Chatbot';
import MainPage from './components/MainPage';
import ExercisePlanComponent from './components/ExercisePlanComponent';
import { useNavigate } from 'react-router-dom';
import './App.css';
import { BrowserRouter,Routes,Route }  from 'react-router-dom'
// import RegisterAndLogin from './components/RegisterAndLogin';
// import HomeScreen from './components/Home';
// import ForgotPassword from './components/ForgotPassword'
// import Exercise from './components/Exercise';
function App() {
  const [exerciseData,setExerciseData]=useState(""); 
  // const history=useNavigate()
  return (
    <>
    <BrowserRouter>
      <div>
      <Routes>
        {/* <Route path="/" element={<RegisterAndLogin/>}/> */}
        {/* <Route path="/home" element={<HomeScreen/>}/> */}
        {/* <Route path="/reset" element={<ForgotPassword/>} /> */}
        <Route path="/" element={<MainPage/>} />
        <Route path="/livefeed/:exerciseType" element={<LiveFeed/>} />

        

      </Routes>
      <Chatbot/>
      </div>
    </BrowserRouter>
    </>
  );
}
 
export default App;
  