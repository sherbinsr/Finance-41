import React from "react";
import { Button, Container } from "react-bootstrap";
import { Typography } from "@mui/material";
import '../Home/Home.css';
import About from '../About/About';
import ContactUs  from "../Contactus/Contactus";
import Footer from "../Footer/Footer";
import UserAnalytics from "../UserAnalytics/UserAnalytics";
import { useNavigate } from 'react-router-dom';

const Home = () => {
  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate('/proxy/3000/chatbot');
  };
  return (
    <div className="ct">
      <div className="app">
        <div className="main-content">
          <Container className="text-center d-flex flex-column align-items-center">
            <Typography variant="h2" className="text-light text-center main-heading">
              Financial Decisions with AI
            </Typography>
            <Typography variant="h5" className="text-light my-3">
              Discover how AI can make your wealth work harder for you.
            </Typography>
            <Button variant="danger" size="lg" className="my-3" onClick={handleButtonClick}  >
             Talk With AI 
            </Button>
            <Typography variant="body1" className="text-light">
              Upgrade your financial strategy today.
            </Typography>
          </Container>
        </div>
      </div>
      <br></br>
      <div className="container">
        <About/>
      </div>
      <div className="container">
        <UserAnalytics/>
      </div>
      <br></br><br></br>
      <div className="container">
        <ContactUs/>
        <br></br> <br></br>
      </div>
      <div>
      <Footer/>
      </div>
               
    </div>
  );
};

export default Home;
