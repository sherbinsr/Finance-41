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
import Portfolio from './components/PortfolioAnalyze/Portfolio';


function App() {
  return (
    <Router>
      <Topbar/>
      <Routes>      
      <Route path="/proxy/3000/" element={<Home/>} />
      <Route path="/proxy/3000/chatbot" element={<Chatbot />} />
      <Route path="/proxy/3000/register" element={<Register />} />
      <Route path="/proxy/3000/login" element={<Login />} />
      <Route path="/proxy/3000/home/:id" element={<Home />} />
      <Route path="/proxy/3000/contactus" element={<ContactUs/>}/> 
      <Route path="/proxy/3000/news" element={<News/>}/> 
      <Route path="/proxy/3000/trends" element={<MarketTrends/>}/> 
      <Route path="/proxy/3000/stockinfo" element={<StockInfo/>}/> 
      <Route path="/proxy/3000/portfolio" element={<Portfolio/>}/>
      <Route path="/proxy/3000/404" element={<NotFound/>}/> 
      </Routes>
    </Router>
  );
}

export default App;
