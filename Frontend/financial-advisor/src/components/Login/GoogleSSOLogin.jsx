import React from 'react';

function  GoogleSSOLogin() {
  const handleLogin = () => {
    window.open("https://finance-41-1081098542602.us-central1.run.app/proxy/8000/sso-login", "_self");
   
};

return (
    <div className='text-center'>
       <button className='btn btn-primary w-80' onClick={handleLogin}>Login with Google</button>
    </div>
);
}

export default GoogleSSOLogin;
