import React, { useState } from 'react';

const ContactUs = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    company: '',
    email: '',
    phoneNumber: '',
    message: '',
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log(formData);
  };

  return (
    <div className="container mt-3" style={{ maxWidth: '600px' }}>
      <h1 className="text-center fw-bold text-danger">Contact Us</h1>
      <form onSubmit={handleSubmit} className="p-3 shadow-sm">
        <div className="row mb-2">
          <div className="col-md-6 mb-2">
            <label htmlFor="firstName" className="form-label small">First name</label>
            <input
              type="text"
              className="form-control form-control-sm"
              id="firstName"
              name="firstName"
              value={formData.firstName}
              onChange={handleChange}
              required
            />
          </div>
          <div className="col-md-6 mb-2">
            <label htmlFor="lastName" className="form-label small">Last name</label>
            <input
              type="text"
              className="form-control form-control-sm"
              id="lastName"
              name="lastName"
              value={formData.lastName}
              onChange={handleChange}
              required
            />
          </div>
        </div>
        <div className="mb-2">
          <label htmlFor="email" className="form-label small">Email</label>
          <input
            type="email"
            className="form-control form-control-sm"
            id="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-2">
          <label htmlFor="phoneNumber" className="form-label small">Phone number</label>
          <input
            type="tel"
            className="form-control form-control-sm"
            id="phoneNumber"
            name="phoneNumber"
            value={formData.phoneNumber}
            onChange={handleChange}
            required
          />
        </div>

        <div className="mb-2">
          <label htmlFor="message" className="form-label small">Message</label>
          <textarea
            className="form-control form-control-sm"
            id="message"
            name="message"
            rows="3"
            value={formData.message}
            onChange={handleChange}
            required
          />
        </div>

        <br></br>
        <div className="text-center">
          <button type="submit" className="btn btn-dark btn-sm">Let's talk</button>
        </div>
      </form>
      <br></br> <br></br>
    </div>
  );
};

export default ContactUs;
