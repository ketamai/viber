import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const VerifyEmail = () => {
  const [verified, setVerified] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { verifyEmail, currentUser } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  
  // Extract token from URL if present
  useEffect(() => {
    const queryParams = new URLSearchParams(location.search);
    const token = queryParams.get('token');
    
    if (token) {
      handleVerify(token);
    }
  }, [location]);
  
  const handleVerify = async (token) => {
    try {
      setLoading(true);
      await verifyEmail(token);
      setVerified(true);
    } catch (err) {
      setError('Failed to verify email. The link may be expired or invalid.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };
  
  const handleResendVerification = async () => {
    try {
      setLoading(true);
      await verifyEmail(null, true); // Pass true to indicate resend
      setError('');
      alert('Verification email has been sent!');
    } catch (err) {
      setError('Failed to resend verification email.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="w-full max-w-md text-center">
        <h2 className="text-center text-3xl font-bold mb-6">Email Verification</h2>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}
        
        {verified ? (
          <div>
            <div className="bg-green-100 border border-green-400 text-green-700 px-4 py-3 rounded mb-6">
              Your email has been verified successfully!
            </div>
            <button
              onClick={() => navigate('/dashboard')}
              className="mt-4 py-2 px-6 bg-blue-600 text-white rounded"
            >
              Go to Dashboard
            </button>
          </div>
        ) : (
          <div>
            <p className="mb-6">
              Please verify your email address by clicking the link we sent to your email.
              If you don't see the email, check your spam folder.
            </p>
            
            <button
              onClick={handleResendVerification}
              disabled={loading}
              className="mt-4 py-2 px-6 bg-blue-600 text-white rounded"
            >
              {loading ? 'Processing...' : 'Resend Verification Email'}
            </button>
            
            <div className="mt-6">
              <Link to="/login" className="text-blue-600">
                Return to Login
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default VerifyEmail; 