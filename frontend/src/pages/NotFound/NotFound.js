import React from 'react';
import { Link } from 'react-router-dom';

const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="text-center">
        <h1 className="text-6xl font-wow text-wow-gold mb-4">404</h1>
        <h2 className="text-3xl font-semibold text-wow-light mb-6">Page Not Found</h2>
        <p className="text-xl text-wow-light/80 mb-8">
          The page you're looking for doesn't exist or has been moved.
        </p>
        <Link 
          to="/" 
          className="btn-primary inline-block py-3 px-8"
        >
          Return to Home
        </Link>
      </div>
    </div>
  );
};

export default NotFound; 