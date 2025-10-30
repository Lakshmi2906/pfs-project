import React, { useState, useEffect } from 'react';
import { FaPills, FaClock, FaCalendarAlt, FaChartLine, FaExclamationCircle } from 'react-icons/fa';
import { medicineAPI, reminderAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();
  const userId = user?.id;
  const [medicines, setMedicines] = useState([]);
  const [upcomingReminders, setUpcomingReminders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (!userId) {
      setLoading(false);
      return;
    }

    const fetchData = async () => {
      try {
        const [medicinesRes, remindersRes] = await Promise.all([
          medicineAPI.getMedicines(userId),
          reminderAPI.getReminders(userId)
        ]);
        setMedicines(medicinesRes.data);
        setUpcomingReminders(remindersRes.data);
        setError('');
      } catch (error) {
        console.error('Error fetching data:', error);
        setError('Unable to load your data right now. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [userId]);

  if (loading) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        fontSize: '1.2rem'
      }}>
        Loading...
      </div>
    );
  }

  if (!userId) {
    return (
      <div style={{
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        minHeight: '100vh',
        fontSize: '1.2rem',
        textAlign: 'center',
        padding: '2rem'
      }}>
        Please sign in to view your personalized dashboard.
      </div>
    );
  }

  return (
    <div style={{
      backgroundColor: '#f8f9fa',
      minHeight: '100vh',
      paddingTop: '100px',
      padding: '100px 1rem 2rem'
    }}>
      <div style={{maxWidth: '1200px', margin: '0 auto'}}>
        {/* Header */}
        <div style={{textAlign: 'center', marginBottom: '3rem'}}>
          <h1 style={{fontSize: '2.5rem', fontWeight: 'bold', color: '#667eea', marginBottom: '0.5rem'}}>
            Health Dashboard
          </h1>
          <p style={{fontSize: '1.1rem', color: '#6c757d'}}>
            Monitor your medications and stay on track
          </p>
        </div>

        {/* Stats Cards */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
          gap: '1.5rem',
          marginBottom: '3rem'
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '15px',
            padding: '2rem',
            textAlign: 'center',
            boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
            border: '3px solid #667eea'
          }}>
            <FaPills style={{fontSize: '2.5rem', color: '#667eea', marginBottom: '1rem'}} />
            <h3 style={{fontSize: '2rem', fontWeight: 'bold', color: '#667eea', marginBottom: '0.5rem'}}>{medicines.length}</h3>
            <p style={{color: '#6c757d', margin: 0}}>Active Medications</p>
          </div>
          
          <div style={{
            backgroundColor: 'white',
            borderRadius: '15px',
            padding: '2rem',
            textAlign: 'center',
            boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
            border: '3px solid #28a745'
          }}>
            <FaCalendarAlt style={{fontSize: '2.5rem', color: '#28a745', marginBottom: '1rem'}} />
            <h3 style={{fontSize: '2rem', fontWeight: 'bold', color: '#28a745', marginBottom: '0.5rem'}}>{upcomingReminders.length}</h3>
            <p style={{color: '#6c757d', margin: 0}}>Today's Doses</p>
          </div>
          
          <div style={{
            backgroundColor: 'white',
            borderRadius: '15px',
            padding: '2rem',
            textAlign: 'center',
            boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
            border: '3px solid #ffc107'
          }}>
            <FaExclamationCircle style={{fontSize: '2.5rem', color: '#ffc107', marginBottom: '1rem'}} />
            <h3 style={{fontSize: '2rem', fontWeight: 'bold', color: '#ffc107', marginBottom: '0.5rem'}}>{upcomingReminders.filter(r => r.status === 'pending').length}</h3>
            <p style={{color: '#6c757d', margin: 0}}>Pending Reminders</p>
          </div>
          
          <div style={{
            backgroundColor: 'white',
            borderRadius: '15px',
            padding: '2rem',
            textAlign: 'center',
            boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
            border: '3px solid #17a2b8'
          }}>
            <FaChartLine style={{fontSize: '2.5rem', color: '#17a2b8', marginBottom: '1rem'}} />
            <h3 style={{fontSize: '2rem', fontWeight: 'bold', color: '#17a2b8', marginBottom: '0.5rem'}}>--</h3>
            <p style={{color: '#6c757d', margin: 0}}>Adherence Rate</p>
          </div>
        </div>

        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(500px, 1fr))',
          gap: '2rem'
        }}>
          {/* My Medicines */}
          <div style={{
            backgroundColor: 'white',
            borderRadius: '20px',
            boxShadow: '0 15px 35px rgba(0,0,0,0.1)',
            overflow: 'hidden'
          }}>
            <div style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              padding: '1.5rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem'
            }}>
              <FaPills style={{fontSize: '1.5rem'}} />
              <h4 style={{margin: 0, fontSize: '1.25rem', fontWeight: 'bold'}}>My Medicines</h4>
            </div>
            <div>
              {medicines.length > 0 ? medicines.map((med, index) => (
                <div key={index} style={{
                  padding: '1.5rem',
                  borderBottom: index < medicines.length - 1 ? '1px solid #e9ecef' : 'none',
                  transition: 'background-color 0.3s'
                }}
                onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#f8f9fa'}
                onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'white'}>
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start'
                  }}>
                    <div style={{flex: 1}}>
                      <h5 style={{
                        fontWeight: 'bold',
                        marginBottom: '0.5rem',
                        fontSize: '1.1rem'
                      }}>
                        {med.name}
                      </h5>
                      <p style={{
                        color: '#6c757d',
                        marginBottom: '0.75rem',
                        fontSize: '0.9rem'
                      }}>
                        {med.dosage} • {med.frequency}
                      </p>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        color: '#667eea',
                        fontSize: '0.9rem',
                        fontWeight: 'bold'
                      }}>
                        <FaClock style={{marginRight: '0.5rem'}} />
                        Next: {med.next_dose || 'Not set'}
                      </div>
                    </div>
                    <span style={{
                      backgroundColor: '#28a745',
                      color: 'white',
                      padding: '0.25rem 0.75rem',
                      borderRadius: '20px',
                      fontSize: '0.8rem',
                      fontWeight: 'bold'
                    }}>
                      Active
                    </span>
                  </div>
                </div>
              )) : (
                <div style={{padding: '2rem', textAlign: 'center', color: '#6c757d'}}>
                  No medicines found. Upload a prescription to get started.
                </div>
              )}
            </div>
          </div>

          {/* Upcoming Reminders */}
          <div style={{
            backgroundColor: 'white',
            borderRadius: '20px',
            boxShadow: '0 15px 35px rgba(0,0,0,0.1)',
            overflow: 'hidden'
          }}>
            <div style={{
              background: 'linear-gradient(135deg, #28a745 0%, #20c997 100%)',
              color: 'white',
              padding: '1.5rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.75rem'
            }}>
              <FaCalendarAlt style={{fontSize: '1.5rem'}} />
              <h4 style={{margin: 0, fontSize: '1.25rem', fontWeight: 'bold'}}>Upcoming Reminders</h4>
            </div>
            <div>
              {upcomingReminders.length > 0 ? upcomingReminders.map((reminder, index) => (
                <div key={index} style={{
                  padding: '1.5rem',
                  borderBottom: index < upcomingReminders.length - 1 ? '1px solid #e9ecef' : 'none',
                  transition: 'background-color 0.3s'
                }}
                onMouseOver={(e) => e.currentTarget.style.backgroundColor = '#f8f9fa'}
                onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'white'}>
                  <div style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center'
                  }}>
                    <div>
                      <h5 style={{
                        fontWeight: 'bold',
                        marginBottom: '0.5rem',
                        fontSize: '1.1rem'
                      }}>
                        {reminder.medicine_name} {reminder.dosage}
                      </h5>
                      <p style={{
                        color: '#6c757d',
                        margin: 0,
                        fontSize: '0.9rem'
                      }}>
                        {reminder.reminder_time}
                      </p>
                    </div>
                    <span style={{
                      backgroundColor: '#17a2b8',
                      color: 'white',
                      padding: '0.25rem 0.75rem',
                      borderRadius: '20px',
                      fontSize: '0.8rem',
                      fontWeight: 'bold'
                    }}>
                      Auto Call
                    </span>
                  </div>
                </div>
              )) : (
                <div style={{padding: '2rem', textAlign: 'center', color: '#6c757d'}}>
                  No reminders set up yet.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;