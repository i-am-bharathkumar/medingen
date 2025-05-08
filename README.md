# Medingen Medicine Comparison Platform

A React frontend and Flask API backend application that displays medicine comparisons with detailed analytics, salt content information, and user reviews.

## Video Introduction
[View my introduction video](https://drive.google.com/file/d/1hjeaKHhRpSRmIXWG9cTXo6yD060EWxRL/view?usp=sharing)

*This 5-minute video introduces myself, my technical background, and my approach to the Medingen project.*

## Project Overview

This project implements a medicine comparison platform with the following features:
- Medicine details page with comparative salt content analysis
- Alternative medicine suggestions
- User ratings and reviews
- Responsive design for web and mobile
- JWT authentication
- MySQL database integration

## Repository Structure

```
medingen-project/
├── frontend/           # React Application
│   ├── public/         # Public assets
│   └── src/
│       ├── components/ # Reusable UI components
│       │   ├── Header.js
│       │   ├── MedicineDetails.js
│       │   ├── AlternativeMedicines.js
│       │   ├── ComparisonTable.js
│       │   ├── FAQ.js
│       │   ├── RatingReviews.js
│       │   └── Footer.js
│       ├── services/   # API integration
│       │   └── api.js
│       ├── contexts/   # State management
│       │   └── AuthContext.js
│       ├── pages/
│       │   ├── Login.js
│       │   └── MedicinePage.js
│       ├── App.js
│       └── index.js
│
├── backend/            # Flask API
│   ├── app.py          # Main Flask application
│   ├── models.py       # SQLAlchemy models
│   ├── routes/         # API routes
│   │   ├── auth.py
│   │   └── medicines.py
│   ├── config.py       # Configuration
│   └── requirements.txt # Python dependencies
│
└── database/           # MySQL scripts
    └── schema.sql      # Database schema and sample data
```

## Technology Stack

### Frontend
- React (with React Context for state management)
- CSS (responsive design)
- Axios for API requests

### Backend
- Flask (Python web framework)
- Flask-SQLAlchemy (ORM)
- Flask-JWT-Extended (Authentication)
- MySQL (Database)

## Setup Instructions

### Prerequisites
- Node.js (v16.x or later)
- Python (v3.8 or later)
- MySQL (v8.0 or later)

### Database Setup
1. Install MySQL and create a new database:
   ```sql
   CREATE DATABASE medingen;
   ```
2. Import the database schema and sample data:
   ```bash
   mysql -u [username] -p medingen < database/schema.sql
   ```

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd backend
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure the database connection in `config.py` with your MySQL credentials.
5. Run the Flask application:
   ```bash
   python app.py
   ```
   The API will be available at `http://localhost:5000`

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm start
   ```
   The application will be available at `http://localhost:3000`

## API Endpoints

### Authentication
- `POST /api/auth/login`: User authentication endpoint (returns JWT token)

### Medicines
- `GET /api/medicines`: Get list of medicines
- `GET /api/medicines/<id>`: Get detailed information about a specific medicine
- `GET /api/medicines/<id>/alternatives`: Get alternative medicines
- `GET /api/medicines/<id>/reviews`: Get user reviews for a medicine
- `GET /api/medicines/<id>/salts`: Get salt content details

## Features Implemented

1. **Dynamic Data Loading**: All data is loaded from the backend API
2. **Component-Based Architecture**: Reusable React components
3. **Responsive Design**: Optimized for mobile and desktop (up to 1366px)
4. **JWT Authentication**: Secure API endpoints
5. **Normalized Database Design**: Properly structured data models
6. **Modular Backend**: Organized Flask application structure

## Login Credentials

Use the following credentials for the demo:
- Username: `user@medingen.com`
- Password: `password123`

## Notes

- The application uses a local MySQL database with sample data
- Frontend is built with pure CSS (no preprocessors)
- Backend implements proper error handling and validation
- All component rendering is dynamic based on API responses

## Development Decisions

- Used React Context for state management instead of Redux for simplicity
- Implemented JWT authentication with token expiration
- Structured the database in normalized form for data integrity
- Created reusable components to maintain DRY principles
- Used async/await for all API calls with proper error handling

## Future Improvements

- Implement user registration
- Add medicine search functionality
- Enhance the mobile experience
- Add unit and integration tests
- Implement caching for improved performance

## Video Introduction Requirements

As part of the submission requirements, I've recorded a 5-minute video introduction about myself and my approach to this project. The video covers:

1. A brief personal introduction
2. My technical background
3. The approach taken for this project
4. Key design decisions and trade-offs
5. Challenges faced during development

The video is accessible via the Google Drive link at the top of this README.
