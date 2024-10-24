import { Navbar, Nav, Button, Container } from "react-bootstrap";
import React from "react";
import { Typography } from "@mui/material"; 

const Topbar = () => {
  return ( 
    <div>
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
                <Nav.Link href="/proxy/3000/" className="header-link">Home</Nav.Link>
                <Nav.Link href="/proxy/3000/trends" className="header-link">Market Trends</Nav.Link>
                <Nav.Link href="/proxy/3000/chatbot" className="header-link">Talk with AI</Nav.Link>
                <Nav.Link href="/proxy/3000/portfolio" className="header-link">Portfolio Analysis</Nav.Link>
                <Nav.Link href="/proxy/3000/news" className="header-link">News</Nav.Link>
                <Nav.Link href="/proxy/3000/contactus" className="header-link">Contact Us</Nav.Link>
                <Button variant="outline-light" href="/proxy/3000/register" className="ms-md-3">SIGN UP</Button>
              </Nav>
            </Navbar.Collapse>
          </Container>
        </Navbar>
      </header>
    </div>
  );
}

export default Topbar;
