# TourJett - Travel Agency Platform


## Overview

TourJett is a comprehensive travel agency platform that enables users to browse, book, and manage tour packages around the world. Our platform provides an intuitive interface for tourists to explore destinations and make reservations while offering robust management tools for administrators.

## Features

- **User Authentication**: Secure login and registration system
- **Tour Package Browsing**: Browse through various tour packages with filtering options
- **Destination Exploration**: Discover top destinations with detailed information
- **Online Booking System**: Book tours with an easy-to-use interface
- **Special Offers**: View and book special promotional tour packages
- **Blog & News**: Stay updated with the latest travel trends and news
- **Administrative Dashboard**: Comprehensive management of tours, reservations, and customers
- **Reviews & Ratings**: Read and submit reviews for tour experiences

## Tech Stack

### Frontend
- HTML5, CSS3, JavaScript
- Bootstrap for responsive design
- jQuery for DOM manipulation
- Various JS libraries (owl.carousel, filterizr, datepicker)

### Backend
- Python with Flask framework
- SQLAlchemy ORM
- Alembic for database migrations

### Database
- PostgreSQL (via Docker container)

### Deployment
- Docker and Docker Compose for containerization

## Project Structure

```
├── backend/                # Flask backend application
│   ├── app/                # Main application package
│   │   ├── models/         # Database models (SQLAlchemy)
│   │   ├── routes/         # API endpoints
│   │   └── services/       # Business logic layer
│   ├── migrations/         # Database migrations (Alembic)
│   └── static/             # Static assets for backend
├── frontend/               # Frontend application
│   └── TourNest-master/    # HTML templates and assets
└── docker-compose.yml      # Docker-compose configuration
```

## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.11+

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/TourJett.git
   cd TourJett
   ```

2. Build and start the containers
   ```bash
   docker-compose up -d
   ```

3. The application should be running at:
   - Frontend: http://localhost:8080
   - Backend API: http://localhost:5000

### Development Setup

1. Create a virtual environment
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server
   ```bash
   cd backend
   python run.py
   ```

## API Documentation

The API provides endpoints for:
- User Authentication (/auth/*)
- Tour Packages (/tur/*)
- Destinations (/bolge/*)
- Reservations (/rezervasyon/*)
- Reviews (/degerlendirme/*)
- Customer Management (/musteri/*)

Detailed API documentation is available at `/api/docs` when running the backend server.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [ThemeSINE](https://www.themesine.com) for the TourNest HTML template
- All open source libraries and frameworks used in this project

## Contact

For support or inquiries, please contact info@tourjett.com
