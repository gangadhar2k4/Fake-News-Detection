# Fake News Detector

## Overview

The Fake News Detector is a Django-based web application that uses machine learning to analyze news articles and detect potential misinformation. The system employs multiple ML models (Logistic Regression and Decision Tree Classifier) to provide predictions on whether news content is likely true, fake, or partially true. Users can create accounts, verify news articles, track their verification history, and view analytics through a comprehensive dashboard.

## System Architecture

### Backend Architecture
- **Framework**: Django 4.x with Python
- **Database**: SQLite (default Django database, can be upgraded to PostgreSQL)
- **Authentication**: Django's built-in authentication system
- **Machine Learning**: scikit-learn with custom ML pipeline
- **Text Processing**: TF-IDF vectorization with custom text preprocessing

### Frontend Architecture
- **Template Engine**: Django templates with Jinja2 syntax
- **CSS Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **Charts**: Chart.js for data visualization
- **JavaScript**: Vanilla JavaScript for interactive features

### Application Structure
The application follows Django's app-based architecture with three main apps:
- **accounts**: User authentication and registration
- **dashboard**: User analytics and overview
- **verifier**: News verification and history management

## Key Components

### User Authentication System
- **Registration**: Custom signup form with extended user fields (first name, last name, email)
- **Login/Logout**: Django's built-in authentication views with custom templates
- **Access Control**: Login-required decorators protect authenticated routes

### Machine Learning Pipeline
- **Text Preprocessing**: Custom TextPreprocessor class handles cleaning, URL removal, and text normalization
- **Models**: Dual-model approach using Logistic Regression and Decision Tree Classifier
- **Feature Extraction**: TF-IDF vectorization for text-to-numeric conversion
- **Prediction Logic**: Ensemble approach combining multiple model outputs

### Data Models
- **VerificationResult**: Stores user verification history with title, content, prediction, confidence, category, and bookmarking
- **TrendingTopic**: Tracks popular verification topics with usage counts
- **User**: Extended Django User model for authentication

### Dashboard Analytics
- **Statistics**: Total checks, true/fake news counts, bookmarked articles
- **Recent Activity**: Latest verification results
- **Trending Topics**: Popular verification categories
- **Visual Charts**: Usage trends and category breakdowns

## Data Flow

### News Verification Process
1. User submits news content through verification form
2. Text preprocessing cleans and normalizes input
3. TF-IDF vectorizer converts text to numerical features
4. Multiple ML models generate predictions with confidence scores
5. Results are saved to user's history (if opted in)
6. Trending topics are updated based on category and content
7. User receives detailed analysis with model-specific predictions

### User Dashboard Updates
1. Dashboard queries user's verification history
2. Statistics are calculated dynamically from database
3. Recent checks and trending topics are fetched
4. Data is rendered through Django templates with Chart.js visualization

## External Dependencies

### Python Packages
- **Django**: Web framework and ORM
- **scikit-learn**: Machine learning models and preprocessing
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computations
- **joblib**: Model serialization and loading

### Frontend Libraries
- **Bootstrap 5.3.0**: UI components and responsive design
- **Font Awesome 6.4.0**: Icon library
- **Chart.js**: Interactive charts and graphs

### Training Data
- **Sample Data**: Built-in training dataset with real and fake news examples
- **Model Training**: Offline training script with model persistence
- **Data Augmentation**: Additional training data for improved accuracy

## Deployment Strategy

### Development Setup
- **Database**: SQLite for local development
- **Static Files**: Django's static file handling
- **Debug Mode**: Enabled with detailed error pages
- **Secret Key**: Environment variable with fallback

### Production Considerations
- **Database**: Upgrade to PostgreSQL for production scale
- **Static Files**: Configure proper static file serving
- **Security**: Disable debug mode, secure secret keys
- **Model Storage**: Persistent storage for trained ML models
- **Performance**: Consider caching for frequent database queries

### Environment Configuration
- **Settings**: Environment-based configuration
- **Allowed Hosts**: Configured for deployment platforms
- **WSGI**: Production-ready WSGI configuration

## Changelog
- June 29, 2025. Initial setup

## User Preferences

Preferred communication style: Simple, everyday language.