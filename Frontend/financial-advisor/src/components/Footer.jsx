import React from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Footer.css'; 
import logo from '../assets/logo.png'; 

function Footer() {
  return (
    <footer className="footer bg-dark text-white text-center py-4">
    <div className="container">
        <img  src={logo} alt="Company Logo" className="footer-logo mb-3" />
     
        <div className="contact-details mt-3">
            <p>Email: finance41@41.com</p>
            <p>Phone: +91 9677472562</p>
        </div>
        <p className="mb-0">© 2024 Your Company Name. All rights reserved.</p>
    </div>
</footer>
  );

}
export default Footer;