# MediTrack - Healthcare Management Application

A React-based healthcare application for managing medications, prescriptions, and reminders.

## Features

- **Home Page**: Welcome page with 4 feature cards (Smart Reminders, Prescription Upload, Pill Identification, Refill Alerts)
- **Authentication**: Login and Signup pages with form validation
- **Dashboard**: View parsed medicines and upcoming reminders
- **Upload Interface**: Upload prescriptions and pill images with drag-and-drop functionality
- **Responsive Design**: Mobile-friendly interface
- **React Router**: Navigation between pages
- **React Icons**: Beautiful UI icons throughout the application

## Project Structure

```
src/
├── components/
│   └── Navbar.js          # Navigation component
├── pages/
│   ├── Home.js            # Home page with feature cards
│   ├── Login.js           # Login form
│   ├── Signup.js          # Registration form
│   ├── Dashboard.js       # Medicine and reminder dashboard
│   └── Upload.js          # File upload interface
├── styles/
│   └── index.css          # All CSS styles
├── App.js                 # Main app component with routing
└── index.js               # React entry point
```

## Installation & Setup

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

3. Open [http://localhost:3000](http://localhost:3000) to view the application.

## Technologies Used

- React 18
- React Router DOM
- React Icons
- CSS3 (Flexbox & Grid)
- Responsive Design

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner

## Features Overview

### Home Page
- Hero section with call-to-action
- 4 feature cards linking to relevant pages
- Responsive grid layout

### Authentication
- Login/Signup forms with icons
- Form validation
- Responsive design

### Dashboard
- Medicine list with dosage information
- Upcoming reminders with status badges
- Clean card-based layout

### Upload Interface
- Tabbed interface for prescriptions vs pill identification
- Drag-and-drop file upload
- File type validation

## Responsive Design
The application is fully responsive and works on:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)