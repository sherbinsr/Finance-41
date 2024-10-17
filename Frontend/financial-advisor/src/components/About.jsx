import about from "../assets/about.jpg"
import React from "react";


function About() {
    return (
        <div className="container my-5">
        <div className="row align-items-center">
              {/* Image Section */}
              <div className="col-lg-6 col-md-12 mb-4 mb-lg-0">
                <img
                  src={about}
                  alt="Event"
                  className="img-fluid w-100"
                  style={{ borderRadius: "15px" }}
                />
              </div>
        
              {/* Text Section */}
              <div className="col-lg-6 col-md-12 text-center text-lg-start">
              <h1 className="fw-bold text-danger">Unlock Smarter Financial Decisions with AI</h1>
                <p style={{ fontSize: "16px", color: "#4f4f4f" }}>
                Unlock smarter financial decisions with our AI-Powered Financial Advisor, designed to help you manage your wealth effectively. Our AI delivers tailored insights and real-time recommendations for retirement planning, investing, and budget optimization based on your unique goals. Benefit from expert investment strategies and budget tools that identify savings opportunities while monitoring market trends. Seamlessly connect your accounts to our secure platform, ensuring data protection and access to an interactive dashboard. Take control of your financial future today and experience the potential for lasting prosperity.
                </p>
              </div>
            </div>
          </div>
    )
  }
  export default About;
  