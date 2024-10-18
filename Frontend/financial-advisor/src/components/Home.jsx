import React from "react";
import { Navbar, Nav, Button, Container } from "react-bootstrap";
import { Typography } from "@mui/material";
import './Home.css';
import About from './About';
import ContactUs  from "./Contactus";
import Footer from "./Footer";


const Home = () => {
  return (
    <div className="ct">
      <div className="app">
        <header className="header">
          <Navbar expand="md" bg="dark" variant="dark" className="p-3">
            <Container fluid>
              <Navbar.Brand>
                <Typography variant="h5" className="text-light">
                  FINANCE 41
                </Typography>
              </Navbar.Brand>
              <Navbar.Toggle aria-controls="basic-navbar-nav" />
              <Navbar.Collapse id="basic-navbar-nav" className="justify-content-center">
                <Nav className="header-links">
                  <Nav.Link href="#" className="header-link">Home</Nav.Link>
                  <Nav.Link href="#" className="header-link">Market Trends </Nav.Link>
                  <Nav.Link href="/chatbot" className="header-link">Talk with AI</Nav.Link>
                  <Nav.Link href="/news" className="header-link">News </Nav.Link>
                  <Nav.Link href="/contactus" className="header-link">Contact Us</Nav.Link>
                  <Button variant="outline-light" href="/register" className="ms-md-3">SIGN UP</Button>
                </Nav>
              </Navbar.Collapse>
            </Container>
          </Navbar>
        </header>

        <div className="main-content">
          <Container className="text-center d-flex flex-column align-items-center">
            <Typography variant="h2" className="text-light text-center main-heading">
              Financial Decisions with AI
            </Typography>
            <Typography variant="h5" className="text-light my-3">
              Discover how AI can make your wealth work harder for you.
            </Typography>
            <Button variant="danger" size="lg" className="my-3">
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
        <ContactUs/>
      </div>
      <div>
      <Footer/>
      </div>
               
    </div>
  );
};

export default Home;
