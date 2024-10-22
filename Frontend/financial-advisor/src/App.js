import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Chatbot from './components/ChatBot/Chatbot';
import Register from './components/Register/Register';
import Login  from './components/Login/Login';
import Home  from './components/Home/Home'
import ContactUs  from './components/Contactus/Contactus';
import News from './components/News/News';
import Topbar  from './components/Topbar/Topbar';
import NotFound from './components/NotFound/NotFound';
import MarketTrends from './components/MarketTrends/MarketTrends'
import StockInfo from './components/MarketTrends/StockInfo';


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
      <Route path="/news" element={<News/>}/> 
      <Route path="/trends" element={<MarketTrends/>}/> 
      <Route path="/stockinfo" element={<StockInfo/>}/> 
      <Route path="/404" element={<NotFound/>}/> 
      </Routes>
    </Router>
  );
}

export default App;
