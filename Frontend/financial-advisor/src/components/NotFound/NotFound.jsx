import React from 'react';

const NotFound = () => {
  return (
    <div style={styles.container}>
      <h1 style={styles.heading}>404</h1>
      <p style={styles.text}>Oops! I think you have already registered.</p>
      <a href="/" style={styles.link}>Go back to Home</a>
    </div>
  );
};

const styles = {
  container: {
    display: 'flex',
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
    height: '100vh',
    backgroundColor: '#f8f9fa',
  },
  heading: {
    fontSize: '72px',
    marginBottom: '20px',
  },
  text: {
    fontSize: '24px',
    marginBottom: '30px',
  },
  link: {
    fontSize: '18px',
    color: '#007bff',
    textDecoration: 'none',
  }
};

export default NotFound;
