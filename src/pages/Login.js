import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaEnvelope, FaLock, FaHeartbeat } from 'react-icons/fa';
import { authAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

const Login = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();
  const { login } = useAuth();

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const response = await authAPI.login(formData);
      login(response.data.user, response.data.token);
      navigate('/dashboard');
    } catch (err) {
      setError(err.response?.data?.error || 'Login failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.8), rgba(118, 75, 162, 0.8)), url(https://images.unsplash.com/photo-1576091160399-112ba8d25d1f?w=1200&h=800&fit=crop)',
      backgroundSize: 'cover',
      backgroundPosition: 'center',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '2rem 1rem',
      paddingTop: '6rem'
    }}>
      <div style={{
        backgroundColor: 'white',
        borderRadius: '20px',
        padding: '3rem',
        boxShadow: '0 20px 40px rgba(0,0,0,0.1)',
        width: '100%',
        maxWidth: '400px'
      }}>
        <div style={{textAlign: 'center', marginBottom: '2rem'}}>
          <FaHeartbeat style={{fontSize: '3rem', color: '#667eea', marginBottom: '1rem'}} />
          <h2 style={{fontSize: '1.8rem', fontWeight: 'bold', marginBottom: '0.5rem'}}>
            Welcome Back
          </h2>
          <p style={{color: '#6c757d'}}>Sign in to your MediTrack account</p>
        </div>
        
        {error && (
          <div style={{
            backgroundColor: '#f8d7da',
            color: '#721c24',
            padding: '0.75rem',
            borderRadius: '10px',
            marginBottom: '1rem',
            textAlign: 'center'
          }}>
            {error}
          </div>
        )}
        
        <form onSubmit={handleSubmit}>
          <div style={{marginBottom: '1.5rem'}}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              border: '2px solid #e9ecef',
              borderRadius: '10px',
              padding: '0.75rem',
              transition: 'border-color 0.3s'
            }}>
              <FaEnvelope style={{color: '#6c757d', marginRight: '0.75rem'}} />
              <input
                type="email"
                name="email"
                placeholder="Enter your email"
                value={formData.email}
                onChange={handleChange}
                style={{
                  border: 'none',
                  outline: 'none',
                  flex: 1,
                  fontSize: '1rem'
                }}
                required
              />
            </div>
          </div>
          
          <div style={{marginBottom: '2rem'}}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              border: '2px solid #e9ecef',
              borderRadius: '10px',
              padding: '0.75rem',
              transition: 'border-color 0.3s'
            }}>
              <FaLock style={{color: '#6c757d', marginRight: '0.75rem'}} />
              <input
                type="password"
                name="password"
                placeholder="Enter your password"
                value={formData.password}
                onChange={handleChange}
                style={{
                  border: 'none',
                  outline: 'none',
                  flex: 1,
                  fontSize: '1rem'
                }}
                required
              />
            </div>
          </div>
          
          <button 
            type="submit" 
            disabled={loading}
            style={{
              width: '100%',
              background: loading ? '#ccc' : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '50px',
              padding: '1rem',
              fontSize: '1rem',
              fontWeight: 'bold',
              cursor: loading ? 'not-allowed' : 'pointer',
              transition: 'transform 0.3s'
            }}
            onMouseOver={(e) => !loading && (e.target.style.transform = 'translateY(-2px)')}
            onMouseOut={(e) => !loading && (e.target.style.transform = 'translateY(0)')}
          >
            {loading ? 'Signing In...' : 'Sign In'}
          </button>
        </form>
        
        <div style={{textAlign: 'center', marginTop: '1.5rem'}}>
          <p style={{color: '#6c757d'}}>
            Don't have an account? 
            <Link 
              to="/signup" 
              style={{
                color: '#667eea',
                textDecoration: 'none',
                fontWeight: 'bold',
                marginLeft: '0.25rem'
              }}
            >
              Sign up here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Login;