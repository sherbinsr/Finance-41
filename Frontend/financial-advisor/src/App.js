import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chatbot from './components/Chatbot';
import Register from './components/Register';
import Login  from './components/Login';
import Home  from './components/Home'
import ContactUs  from './components/Contactus';
import News from './components/News';
import Topbar  from './components/Topbar';
import UserAnalytics from './components/UserAnalytics';


function App() {
  return (
    <Router>
      <Topbar/>
      <Routes>      
      <Route path="/" element={<Home/>} />
      <Route path="/chatbot" element={<Chatbot />} />
      <Route path="/register" element={<Register />} />
      <Route path="/login" element={<Login />} />
      <Route path="/home/:id" element={<Home />} />
      <Route path="/contactus" element={<ContactUs/>}/> 
      <Route path="/users" element={<UserAnalytics/>}/> 
      <Route path="/news" element={<News/>}/> 
      </Routes>
    </Router>
  );
}

export default App;
