import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { FaUpload, FaCamera, FaFileImage, FaCloudUploadAlt } from 'react-icons/fa';
import { prescriptionAPI } from '../services/api';
import { useAuth } from '../context/AuthContext';

const Upload = () => {
  const [uploadType, setUploadType] = useState('prescription');
  const [dragActive, setDragActive] = useState(false);
  const { user } = useAuth();
  const navigate = useNavigate();

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    const files = e.dataTransfer.files;
    console.log('Files dropped:', files);
  };

  const handleFileSelect = async (e) => {
    const files = e.target.files;
    if (files.length > 0) {
      await uploadFile(files[0], uploadType);
    }
  };

  const uploadFile = async (file, type) => {
    try {
      console.log('Uploading file:', file.name, 'Type:', type);
      
      const formData = new FormData();
      formData.append('file', file);
      formData.append('user_id', user?.id || 1);
      formData.append('type', type);
      
      console.log('Making request to backend...');
      const response = await fetch('http://localhost:5000/api/upload-prescription', {
        method: 'POST',
        body: formData
      });
      
      console.log('Response status:', response.status);
      const result = await response.json();
      console.log('Backend response:', result);
      
      if (result.success) {
        if (type === 'pill') {
          if (result.matches && result.matches.length > 0) {
            const pill = result.matches[0];
            const message = `🔍 PILL IDENTIFICATION RESULT\n\n` +
              `💊 Name: ${pill.drug_name}\n` +
              `🧬 Generic: ${pill.generic_name || 'N/A'}\n` +
              `🎯 Confidence: ${(pill.confidence * 100).toFixed(1)}%\n` +
              `🏥 Condition: ${pill.medical_condition || 'N/A'}\n` +
              `⚠️ Side Effects: ${pill.side_effects ? pill.side_effects.substring(0, 100) + '...' : 'Not available'}\n\n` +
              `✅ Medicine added to your dashboard!`;
            alert(message);
          } else {
            alert('No pill matches found. Please try a clearer image.');
          }
          
          setTimeout(() => {
            navigate('/dashboard');
          }, 2000);
        } else {
          // Prescription processed successfully - redirect to dashboard
          alert(`Prescription processed! Found ${result.saved_count} medicines. Redirecting to dashboard...`);
          setTimeout(() => {
            navigate('/dashboard');
          }, 2000);
        }
      } else {
        alert('Processing failed: ' + result.error);
      }
    } catch (error) {
      console.error('Upload error:', error);
      alert('Upload failed: ' + error.message);
    }
  };

  return (
    <div style={{
      backgroundColor: '#f8f9fa',
      minHeight: '100vh',
      paddingTop: '100px',
      padding: '100px 1rem 2rem'
    }}>
      <div style={{maxWidth: '1000px', margin: '0 auto'}}>
        {/* Header */}
        <div style={{textAlign: 'center', marginBottom: '3rem'}}>
          <h1 style={{fontSize: '2.5rem', fontWeight: 'bold', color: '#667eea', marginBottom: '0.5rem'}}>
            Upload Documents
          </h1>
          <p style={{fontSize: '1.1rem', color: '#6c757d'}}>
            Upload prescriptions or pill images for identification
          </p>
        </div>

        {/* Tab Navigation */}
        <div style={{
          display: 'flex',
          justifyContent: 'center',
          marginBottom: '3rem'
        }}>
          <div style={{
            backgroundColor: 'white',
            borderRadius: '15px',
            padding: '0.5rem',
            boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
            display: 'flex'
          }}>
            <button 
              style={{
                backgroundColor: uploadType === 'prescription' ? '#667eea' : 'transparent',
                color: uploadType === 'prescription' ? 'white' : '#6c757d',
                border: 'none',
                borderRadius: '10px',
                padding: '1rem 2rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                cursor: 'pointer',
                fontWeight: 'bold',
                transition: 'all 0.3s'
              }}
              onClick={() => setUploadType('prescription')}
            >
              <FaFileImage />
              Prescription Upload
            </button>
            <button 
              style={{
                backgroundColor: uploadType === 'pill' ? '#667eea' : 'transparent',
                color: uploadType === 'pill' ? 'white' : '#6c757d',
                border: 'none',
                borderRadius: '10px',
                padding: '1rem 2rem',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                cursor: 'pointer',
                fontWeight: 'bold',
                transition: 'all 0.3s'
              }}
              onClick={() => setUploadType('pill')}
            >
              <FaCamera />
              Pill Identification
            </button>
          </div>
        </div>

        <div style={{
          backgroundColor: 'white',
          borderRadius: '20px',
          padding: '3rem',
          boxShadow: '0 15px 35px rgba(0,0,0,0.1)'
        }}>
          {/* Upload Type Info */}
          <div style={{textAlign: 'center', marginBottom: '2rem'}}>
            {uploadType === 'prescription' ? (
              <div>
                <FaFileImage style={{fontSize: '3rem', color: '#667eea', marginBottom: '1rem'}} />
                <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '0.5rem'}}>
                  Upload Prescription
                </h3>
                <p style={{color: '#6c757d'}}>
                  Upload a photo or scan of your prescription for automatic parsing
                </p>
              </div>
            ) : (
              <div>
                <FaCamera style={{fontSize: '3rem', color: '#17a2b8', marginBottom: '1rem'}} />
                <h3 style={{fontSize: '1.5rem', fontWeight: 'bold', marginBottom: '0.5rem'}}>
                  Pill Identification
                </h3>
                <p style={{color: '#6c757d'}}>
                  Upload a photo of your pill to identify it instantly
                </p>
              </div>
            )}
          </div>

          {/* Upload Zone */}
          <div 
            style={{
              border: `3px dashed ${dragActive ? '#667eea' : '#dee2e6'}`,
              borderRadius: '20px',
              padding: '3rem',
              textAlign: 'center',
              minHeight: '300px',
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              justifyContent: 'center',
              backgroundColor: dragActive ? 'rgba(102, 126, 234, 0.05)' : '#f8f9fa',
              backgroundImage: dragActive ? 'none' : 'url(https://www.google.com/imgres?q=upload%20prescription%20image%20aesthetic&imgurl=https%3A%2F%2Fwww.sprintdiagnostics.in%2Fimages%2Fupload-priscription-img.webp&imgrefurl=https%3A%2F%2Fwww.sprintdiagnostics.in%2Fupload-prescription&docid=ip66TpkZzC1k5M&tbnid=O72-1c3BdZM8OM&vet=12ahUKEwir5Za3mq2QAxU_yjgGHTNlEikQM3oECG8QAA..i&w=632&h=761&hcb=2&ved=2ahUKEwir5Za3mq2QAxU_yjgGHTNlEikQM3oECG8QAA)',
              backgroundSize: 'cover',
              backgroundPosition: 'center',
              transition: 'all 0.3s',
              cursor: 'pointer'
            }}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <FaCloudUploadAlt 
              style={{
                fontSize: '4rem',
                color: dragActive ? '#667eea' : '#6c757d',
                marginBottom: '1.5rem'
              }}
            />
            <h4 style={{
              fontSize: '1.25rem',
              fontWeight: 'bold',
              marginBottom: '1rem',
              color: dragActive ? '#667eea' : '#495057'
            }}>
              {dragActive ? 'Drop files here' : 'Drag and drop files here'}
            </h4>
            <p style={{color: '#6c757d', marginBottom: '1.5rem'}}>or</p>
            <label style={{
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              color: 'white',
              padding: '1rem 2rem',
              borderRadius: '50px',
              cursor: 'pointer',
              fontWeight: 'bold',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              border: 'none',
              fontSize: '1rem',
              transition: 'transform 0.3s'
            }}
            onMouseOver={(e) => e.target.style.transform = 'translateY(-2px)'}
            onMouseOut={(e) => e.target.style.transform = 'translateY(0)'}>
              <input 
                type="file" 
                accept="image/*,.pdf" 
                onChange={handleFileSelect}
                style={{display: 'none'}}
              />
              <FaUpload />
              Choose Files
            </label>
            <p style={{
              color: '#6c757d',
              marginTop: '1rem',
              fontSize: '0.9rem'
            }}>
              Supported formats: JPG, PNG, PDF • Max size: 10MB
            </p>
          </div>

          {/* Features */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '2rem',
            marginTop: '3rem'
          }}>
            <div style={{textAlign: 'center'}}>
              <div style={{
                backgroundColor: '#28a745',
                color: 'white',
                borderRadius: '50%',
                width: '60px',
                height: '60px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1rem',
                fontSize: '1.5rem'
              }}>
                <FaUpload />
              </div>
              <h6 style={{fontWeight: 'bold', marginBottom: '0.5rem'}}>Fast Upload</h6>
              <small style={{color: '#6c757d'}}>Quick and secure file processing</small>
            </div>
            
            <div style={{textAlign: 'center'}}>
              <div style={{
                backgroundColor: '#17a2b8',
                color: 'white',
                borderRadius: '50%',
                width: '60px',
                height: '60px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1rem',
                fontSize: '1.5rem'
              }}>
                <FaCamera />
              </div>
              <h6 style={{fontWeight: 'bold', marginBottom: '0.5rem'}}>AI Recognition</h6>
              <small style={{color: '#6c757d'}}>Advanced image recognition technology</small>
            </div>
            
            <div style={{textAlign: 'center'}}>
              <div style={{
                backgroundColor: '#ffc107',
                color: 'white',
                borderRadius: '50%',
                width: '60px',
                height: '60px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1rem',
                fontSize: '1.5rem'
              }}>
                <FaFileImage />
              </div>
              <h6 style={{fontWeight: 'bold', marginBottom: '0.5rem'}}>Multiple Formats</h6>
              <small style={{color: '#6c757d'}}>Support for various file types</small>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Upload;