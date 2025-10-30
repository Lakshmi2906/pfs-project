import React from 'react';
import { Link } from 'react-router-dom';
import { FaBell, FaUpload, FaPills, FaExclamationTriangle, FaArrowRight } from 'react-icons/fa';

const Home = () => {
  const features = [
    {
      icon: <FaBell style={{color: '#667eea'}} />,
      title: 'Smart Reminders',
      description: 'Never miss a dose with intelligent medication reminders',
      link: '/dashboard',
      image: 'https://images.unsplash.com/photo-1559757148-5c350d0d3c56?w=400&h=250&fit=crop&crop=center'
    },
    {
      icon: <FaUpload style={{color: '#28a745'}} />,
      title: 'Prescription Upload',
      description: 'Upload and digitize your prescriptions instantly',
      link: '/upload',
      image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTSYIfHTUO4umb299GvqcscyEn8QexADGKQFw&s'
    },
    {
      icon: <FaPills style={{color: '#206e7aff'}} />,
      title: 'Pill Identification',
      description: 'Identify pills by uploading photos',
      link: '/upload',
      image: 'https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=400&h=250&fit=crop&crop=center'
    },
    {
      icon: <FaExclamationTriangle style={{color: '#ffc107'}} />,
      title: 'Refill Alerts',
      description: 'Get notified when it\'s time to refill medications',
      link: '/dashboard',
      image: 'https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=400&h=250&fit=crop&crop=center'
    }
  ];

  return (
    <div style={{paddingTop: '80px'}}>
      {/* Hero Section */}
      <div style={{
        background: 'linear-gradient(135deg, rgba(102, 126, 234, 0.9), rgba(118, 75, 162, 0.9)), url(https://images.unsplash.com/photo-1576091160550-2173dba999ef?w=1200&h=800&fit=crop&crop=center)',
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        color: 'white',
        padding: '6rem 1rem',
        textAlign: 'center'
      }}>
        <div style={{maxWidth: '800px', margin: '0 auto'}}>
          <h1 style={{fontSize: '3.5rem', fontWeight: 'bold', marginBottom: '1rem'}}>
            Welcome to MediTrack
          </h1>
          <p style={{fontSize: '1.2rem', marginBottom: '2rem', opacity: 0.9}}>
            Your personal healthcare management companion for a healthier tomorrow
          </p>
          <Link to="/signup" style={{
            backgroundColor: 'white',
            color: '#6270abff',
            padding: '1rem 2rem',
            borderRadius: '50px',
            textDecoration: 'none',
            fontWeight: 'bold',
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.5rem',
            boxShadow: '0 4px 15px rgba(0,0,0,0.2)',
            transition: 'transform 0.3s'
          }}
          onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
          onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}>
            Get Started <FaArrowRight />
          </Link>
        </div>
      </div>
      
      {/* Features Section */}
      <div style={{padding: '4rem 1rem', backgroundColor: '#f8f9fa'}}>
        <div style={{maxWidth: '1200px', margin: '0 auto'}}>
          <div style={{textAlign: 'center', marginBottom: '3rem'}}>
            <h2 style={{fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '1rem'}}>
              Powerful Features
            </h2>
            <p style={{fontSize: '1.1rem', color: '#6c757d'}}>
              Everything you need to manage your health effectively
            </p>
          </div>
          
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
            gap: '2rem'
          }}>
            {features.map((feature, index) => (
              <Link 
                to={feature.link} 
                key={index} 
                style={{
                  backgroundColor: 'white',
                  borderRadius: '15px',
                  overflow: 'hidden',
                  boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
                  textDecoration: 'none',
                  color: 'inherit',
                  transition: 'transform 0.3s, box-shadow 0.3s',
                  height: '100%'
                }}
                onMouseOver={(e) => {
                  e.currentTarget.style.transform = 'translateY(-10px)';
                  e.currentTarget.style.boxShadow = '0 20px 40px rgba(0,0,0,0.15)';
                }}
                onMouseOut={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 10px 30px rgba(0,0,0,0.1)';
                }}
              >
                <div style={{position: 'relative'}}>
                  <img 
                    src={feature.image} 
                    alt={feature.title}
                    style={{
                      width: '100%',
                      height: '200px',
                      objectFit: 'cover'
                    }}
                  />
                  <div style={{
                    position: 'absolute',
                    top: '1rem',
                    right: '1rem',
                    backgroundColor: 'white',
                    borderRadius: '50%',
                    padding: '0.75rem',
                    boxShadow: '0 2px 10px rgba(0,0,0,0.1)'
                  }}>
                    <div style={{fontSize: '1.5rem'}}>{feature.icon}</div>
                  </div>
                </div>
                <div style={{padding: '1.5rem'}}>
                  <h3 style={{fontSize: '1.25rem', fontWeight: 'bold', marginBottom: '0.75rem'}}>
                    {feature.title}
                  </h3>
                  <p style={{color: '#6c757d', marginBottom: '1rem', lineHeight: 1.6}}>
                    {feature.description}
                  </p>
                  <div style={{
                    color: '#667eea',
                    fontWeight: 'bold',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem'
                  }}>
                    Learn More <FaArrowRight />
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>

      {/* Stats Section */}
      <div style={{
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white',
        padding: '3rem 1rem'
      }}>
        <div style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '2rem',
          textAlign: 'center'
        }}>
          <div>
            <h3 style={{fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem'}}>10K+</h3>
            <p style={{opacity: 0.9}}>Active Users</p>
          </div>
          <div>
            <h3 style={{fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem'}}>50K+</h3>
            <p style={{opacity: 0.9}}>Prescriptions Managed</p>
          </div>
          <div>
            <h3 style={{fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem'}}>99.9%</h3>
            <p style={{opacity: 0.9}}>Uptime</p>
          </div>
          <div>
            <h3 style={{fontSize: '2.5rem', fontWeight: 'bold', marginBottom: '0.5rem'}}>24/7</h3>
            <p style={{opacity: 0.9}}>Support</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Home;