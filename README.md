# Modern Ecommerce Platform

A cutting-edge ecommerce platform built with FastAPI, featuring modern payment methods, AI-powered recommendations, and a scalable microservices architecture.

## 🚀 Features

### Core Features
- **User Authentication**: JWT-based authentication for customers and admins
- **Product Management**: Complete CRUD operations for products, categories, and inventory
- **Shopping Cart**: Persistent cart with real-time updates
- **Order Management**: Complete order lifecycle management
- **Admin Dashboard**: Comprehensive admin interface for store management

### Modern Payment Methods
- **Stripe Integration**: Credit/debit cards, digital wallets
- **PayPal**: Express checkout and standard payments
- **Cryptocurrency**: Bitcoin, Ethereum, and other major cryptocurrencies
- **Buy Now, Pay Later**: Klarna and Afterpay integration
- **Digital Wallets**: Apple Pay, Google Pay, Samsung Pay

### AI Recommendation System
- **Collaborative Filtering**: User-based and item-based recommendations
- **Content-Based Filtering**: Product similarity and feature matching
- **Real-time Personalization**: Dynamic recommendations based on user behavior
- **Trend Analysis**: Popular products and seasonal recommendations

### Technical Features
- **RESTful API**: FastAPI with automatic documentation
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Caching**: Redis for performance optimization
- **Real-time Updates**: WebSocket support for live features
- **Image Processing**: Automatic image optimization and CDN integration
- **Email Notifications**: Transactional emails and marketing campaigns

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL
- **Cache**: Redis
- **ORM**: SQLAlchemy
- **Authentication**: JWT
- **Payments**: Stripe, PayPal, Web3

### AI/ML
- **Machine Learning**: Scikit-learn
- **Data Processing**: Pandas, NumPy
- **Recommendations**: Collaborative filtering, content-based filtering

### Frontend (Separate Repository)
- **Framework**: React with TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Redux Toolkit
- **UI Components**: Headless UI, Radix UI

## 📦 Installation

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 6+
- Node.js 18+ (for frontend)

### Backend Setup

1. **Clone the repository**
```bash
git clone <repository-url>
cd ecommerce
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

4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Database Setup**
```bash
# Create database
createdb ecommerce_db

# Run migrations
alembic upgrade head
```

6. **Start the server**
```bash
uvicorn app.main:app --reload
```

### Frontend Setup

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the root directory:

```env
# Database
DATABASE_URL=postgresql://user:password@localhost/ecommerce_db
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Payment APIs
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
PAYPAL_CLIENT_ID=your-paypal-client-id
PAYPAL_CLIENT_SECRET=your-paypal-secret

# Email
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# AI/ML
RECOMMENDATION_MODEL_PATH=models/recommendation_model.pkl
```

## 📚 API Documentation

Once the server is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🏗️ Project Structure

```
ecommerce/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database connection
│   ├── models/                # SQLAlchemy models
│   ├── schemas/               # Pydantic schemas
│   ├── api/                   # API routes
│   ├── core/                  # Core functionality
│   ├── services/              # Business logic
│   ├── utils/                 # Utility functions
│   └── ai/                    # AI recommendation system
├── alembic/                   # Database migrations
├── tests/                     # Test files
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
└── README.md                 # This file
```

## 🧪 Testing

Run tests with pytest:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app
```

## 🚀 Deployment

### Docker Deployment

1. **Build the image**
```bash
docker build -t ecommerce-app .
```

2. **Run with Docker Compose**
```bash
docker-compose up -d
```

### Production Deployment

1. **Set up production environment variables**
2. **Configure reverse proxy (Nginx)**
3. **Set up SSL certificates**
4. **Configure monitoring and logging**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, email support@ecommerce.com or create an issue in the repository. 