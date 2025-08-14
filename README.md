# ARTMANDI - Django Backend API

> Robust Django REST API powering the ARTMANDI online art auction platform

## 🎨 About ARTMANDI API

ARTMANDI API is the backbone of our online art auction platform, built with Django and Django REST Framework. It provides secure, scalable endpoints for managing artwork, auctions, bidding, user authentication, and real-time communications.

## 🏗 Architecture Overview

- **RESTful API Design** - Clean, intuitive endpoints following REST principles
- **Real-time Features** - WebSocket integration for live bidding
- **Microservices Ready** - Modular design for easy scaling
- **Security First** - JWT authentication, rate limiting, and data validation
- **Database Agnostic** - Works with PostgreSQL, MySQL, or SQLite

## ✨ Core Features

### Authentication & User Management
- JWT-based authentication with refresh tokens
- Role-based access control (Buyer, Seller, Admin)
- Social authentication (Google, Facebook)
- Email verification and password reset
- User profile management with KYC verification

### Artwork Management
- Artwork listing with detailed metadata
- Image upload with multiple formats support
- Category and tag management
- Artist profile and portfolio management
- Artwork condition and provenance tracking

### Auction System
- Live auction creation and management
- Multiple auction types (English, Dutch, Sealed-bid)
- Reserve price and starting bid configuration
- Auction scheduling and automatic closure
- Bid increment rules and validation

### Bidding Engine
- Real-time bid processing with WebSocket
- Automatic bid validation and conflict resolution
- Proxy bidding (automatic bidding up to max amount)
- Bid history and analytics
- Anti-sniping protection

### Payment Integration
- Stripe payment processing
- Escrow service integration
- Automatic payment collection
- Refund management
- Commission calculation

### Notification System
- Email notifications for auction events
- Real-time WebSocket notifications
- SMS notifications (optional)
- Push notifications for mobile app

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- PostgreSQL 12+ (recommended) or SQLite for development
- Redis (for caching and WebSocket)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/bilalsiddiqui1311/ArtMandi-FYP-Backend.git
   cd ArtMandi-FYP-Backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   
7. **Start Development Server**
   ```bash
   python manage.py runserver
   ```

## 🛠 Tech Stack

- **Framework**: Django 4.2+ with Django REST Framework
- **Database**: PostgreSQL (production) / SQLite (development)
- **Caching**: Redis
- **Task Queue**: Celery with Redis broker
- **Authentication**: Django JWT + Social Auth
- **Image Processing**: Pillow + Cloudinary
- **Payment**: Stripe API
- **WebSocket**: Django Channels
- **Email**: Django Email with SMTP
- **API Documentation**: drf-spectacular (OpenAPI/Swagger)
- **Testing**: pytest + Factory Boy
- **Code Quality**: Black, isort, flake8