import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { FaUser, FaEnvelope, FaPhone, FaLock, FaHeartbeat } from 'react-icons/fa';
import { authAPI } from '../services/api';

const Signup = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    password: '',
    confirmPassword: ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccess('');
    
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match');
      setLoading(false);
      return;
    }
    
    try {
      await authAPI.register({
        name: formData.name,
        email: formData.email,
        phone: formData.phone,
        password: formData.password
      });
      setSuccess('Registration successful! Redirecting to login...');
      setTimeout(() => navigate('/login'), 2000);
    } catch (err) {
      setError(err.response?.data?.error || 'Registration failed');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, rgba(17, 153, 142, 0.8), rgba(56, 239, 125, 0.8)), url(https://images.unsplash.com/photo-1559757175-0eb30cd8c063?w=1200&h=800&fit=crop)',
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
        maxWidth: '450px'
      }}>
        <div style={{textAlign: 'center', marginBottom: '2rem'}}>
          <FaHeartbeat style={{fontSize: '3rem', color: '#28a745', marginBottom: '1rem'}} />
          <h2 style={{fontSize: '1.8rem', fontWeight: 'bold', marginBottom: '0.5rem'}}>
            Join MediTrack
          </h2>
          <p style={{color: '#6c757d'}}>Create your healthcare account</p>
        </div>
        
        <form onSubmit={handleSubmit}>
          <div style={{marginBottom: '1.5rem'}}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              border: '2px solid #e9ecef',
              borderRadius: '10px',
              padding: '0.75rem'
            }}>
              <FaUser style={{color: '#6c757d', marginRight: '0.75rem'}} />
              <input
                type="text"
                name="name"
                placeholder="Full Name"
                value={formData.name}
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
          
          <div style={{marginBottom: '1.5rem'}}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              border: '2px solid #e9ecef',
              borderRadius: '10px',
              padding: '0.75rem'
            }}>
              <FaEnvelope style={{color: '#6c757d', marginRight: '0.75rem'}} />
              <input
                type="email"
                name="email"
                placeholder="Email Address"
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
          
          <div style={{marginBottom: '1.5rem'}}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              border: '2px solid #e9ecef',
              borderRadius: '10px',
              padding: '0.75rem'
            }}>
              <FaPhone style={{color: '#6c757d', marginRight: '0.75rem'}} />
              <input
                type="tel"
                name="phone"
                placeholder="Phone Number (for reminders)"
                value={formData.phone}
                onChange={handleChange}
                style={{
                  border: 'none',
                  outline: 'none',
                  flex: 1,
                  fontSize: '1rem'
                }}
              />
            </div>
          </div>
          
          <div style={{marginBottom: '1.5rem'}}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              border: '2px solid #e9ecef',
              borderRadius: '10px',
              padding: '0.75rem'
            }}>
              <FaLock style={{color: '#6c757d', marginRight: '0.75rem'}} />
              <input
                type="password"
                name="password"
                placeholder="Password"
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
          
          <div style={{marginBottom: '2rem'}}>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              border: '2px solid #e9ecef',
              borderRadius: '10px',
              padding: '0.75rem'
            }}>
              <FaLock style={{color: '#6c757d', marginRight: '0.75rem'}} />
              <input
                type="password"
                name="confirmPassword"
                placeholder="Confirm Password"
                value={formData.confirmPassword}
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
            style={{
              width: '100%',
              background: 'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '50px',
              padding: '1rem',
              fontSize: '1rem',
              fontWeight: 'bold',
              cursor: 'pointer',
              transition: 'transform 0.3s'
            }}
            onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
            onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}
          >
            Create Account
          </button>
        </form>
        
        <div style={{textAlign: 'center', marginTop: '1.5rem'}}>
          <p style={{color: '#6c757d'}}>
            Already have an account? 
            <Link 
              to="/login" 
              style={{
                color: '#28a745',
                textDecoration: 'none',
                fontWeight: 'bold',
                marginLeft: '0.25rem'
              }}
            >
              Sign in here
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
};

export default Signup;