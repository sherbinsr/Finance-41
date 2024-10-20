import React from 'react';

function  GoogleSSOLogin() {
  const handleLogin = () => {
    window.open("http://127.0.0.1:8000/sso-login", "_self");
   
};

return (
    <div className='text-center'>
       <button className='btn btn-primary w-80' onClick={handleLogin}>Login with Google</button>
    </div>
);
}

export default GoogleSSOLogin;
