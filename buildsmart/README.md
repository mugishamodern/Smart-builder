# BuildSmart - Construction & Home Improvement Platform

BuildSmart is a comprehensive Flask web application that connects users, builders, and service providers in the construction and home improvement ecosystem. The platform facilitates material sourcing, service discovery, and AI-powered project recommendations.

## 🏗️ Features

### Core Functionality
- **User Management**: Multi-role system (customers, shop owners, service providers)
- **Shop Management**: Physical and online construction material shops
- **Product Catalog**: Comprehensive product database with inventory management
- **Service Directory**: Construction and home improvement services
- **Order Management**: Complete order processing and tracking
- **AI Recommendations**: Intelligent project cost estimation and material suggestions
- **Location Services**: Proximity-based shop and service discovery

### Technical Features
- **Flask Application Factory Pattern**: Modular and scalable architecture
- **SQLAlchemy ORM**: Robust database management with migrations
- **Blueprint Organization**: Clean separation of concerns
- **RESTful API**: Comprehensive API for mobile and third-party integrations
- **Error Handling**: Standardized error responses and logging
- **Database Support**: SQLite for development, PostgreSQL for production

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd buildsmart
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   FLASK_APP=app:create_app
   FLASK_ENV=development
   DATABASE_URL=sqlite:///buildsmart.db
   SECRET_KEY=your-secret-key-here
   ```

5. **Initialize the database**
   ```bash
   python -m flask db upgrade
   ```

6. **Run the application**
   ```bash
   python run.py
   ```

The application will be available at `http://localhost:5000`

## 📁 Project Structure

```
buildsmart/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── config.py                # Configuration classes
│   ├── extensions.py            # Flask extensions initialization
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py             # User model with role management
│   │   ├── shop.py             # Shop model with location services
│   │   ├── product.py          # Product model with inventory
│   │   ├── service.py          # Service model for providers
│   │   ├── order.py            # Order and OrderItem models
│   │   └── recommendation.py   # AI recommendation model
│   ├── blueprints/             # Route blueprints
│   │   ├── main/               # Main pages (home, about, contact)
│   │   ├── auth/               # Authentication (login, register)
│   │   ├── user/               # User dashboard and profile
│   │   ├── shop/               # Shop management
│   │   └── api/                # REST API endpoints
│   ├── forms/                  # WTForms for form handling
│   ├── templates/              # Jinja2 templates
│   ├── static/                 # CSS, JS, images
│   ├── utils/                  # Utility functions
│   └── ai/                     # AI recommendation engine
├── migrations/                 # Database migrations
├── tests/                      # Test files
├── requirements.txt            # Python dependencies
├── run.py                     # Application entry point
└── README.md                  # This file
```

## 🗄️ Database Models

### User Model
- **Roles**: customer, shop_owner, service_provider
- **Authentication**: Username/email with password hashing
- **Profile**: Full name, phone, address, location coordinates
- **Relationships**: Shops, services, orders, recommendations

### Shop Model
- **Location**: GPS coordinates for proximity searches
- **Management**: Owner relationship, verification status
- **Metrics**: Rating, review count, product count
- **Relationships**: Products, orders, owner

### Product Model
- **Catalog**: Name, description, category, brand
- **Inventory**: Quantity, availability, pricing
- **Specifications**: JSON field for additional details
- **Relationships**: Shop, order items

### Service Model
- **Provider**: Service provider relationship
- **Details**: Type, hourly rate, experience, certifications
- **Availability**: Service area, availability status
- **Relationships**: Provider

### Order Models
- **Order**: Customer, shop, status, payment information
- **OrderItem**: Individual products with quantities and pricing
- **Tracking**: Order status, delivery information

### Recommendation Model
- **AI Data**: Project type, description, cost estimates
- **Storage**: JSON field for complex recommendation data
- **User**: Personal recommendations per user

## 🔧 Configuration

### Environment Variables
- `FLASK_APP`: Application factory location
- `FLASK_ENV`: Environment (development/production)
- `DATABASE_URL`: Database connection string
- `SECRET_KEY`: Flask secret key for sessions

### Configuration Classes
- **DevelopmentConfig**: Debug mode, SQLite database
- **ProductionConfig**: Production settings, PostgreSQL support
- **TestingConfig**: Test database, disabled CSRF

## 🚀 API Endpoints

### Authentication
- `POST /auth/register` - User registration
- `POST /auth/login` - User login
- `GET /auth/logout` - User logout

### Shops
- `GET /api/shops/nearby` - Find shops near location
- `GET /shop/<id>` - Shop details
- `GET /shop/<id>/products` - Shop products

### Products
- `GET /api/products/search` - Search products
- `GET /api/categories` - Get product categories

### Services
- `GET /api/services/search` - Search services

### Recommendations
- `POST /api/recommend` - Generate AI recommendations

## 🧪 Testing

Run the test suite:
```bash
python -m pytest tests/
```

## 📊 Database Migrations

### Create Migration
```bash
python -m flask db migrate -m "Description of changes"
```

### Apply Migration
```bash
python -m flask db upgrade
```

### Rollback Migration
```bash
python -m flask db downgrade
```

## 🔒 Security Features

- **Password Hashing**: Bcrypt for secure password storage
- **CSRF Protection**: WTForms CSRF tokens
- **Input Validation**: Comprehensive form validation
- **SQL Injection Prevention**: SQLAlchemy ORM protection
- **Role-Based Access**: User type-based permissions

## 🚀 Deployment

### Production Setup
1. Set `FLASK_ENV=production`
2. Configure PostgreSQL database
3. Set secure `SECRET_KEY`
4. Configure reverse proxy (nginx)
5. Use WSGI server (gunicorn)

### Environment Variables for Production
```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@localhost/buildsmart
SECRET_KEY=your-production-secret-key
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📝 Development Guidelines

### Code Style
- Follow PEP 8 guidelines
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions small and focused

### Database Changes
- Always create migrations for schema changes
- Test migrations on development data
- Document breaking changes

### Error Handling
- Use the error handler utilities
- Provide meaningful error messages
- Log errors appropriately

## 🐛 Troubleshooting

### Common Issues

**Database Connection Error**
- Check `DATABASE_URL` in `.env`
- Ensure database exists
- Run migrations: `flask db upgrade`

**Import Errors**
- Activate virtual environment
- Check Python path
- Verify all dependencies installed

**Migration Issues**
- Check model imports in `migrations/env.py`
- Ensure all models are imported
- Try recreating migration

### Getting Help
- Check the logs for error details
- Verify environment variables
- Ensure all dependencies are installed
- Check database connectivity

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Flask framework and ecosystem
- SQLAlchemy for database management
- Flask-Migrate for database migrations
- All contributors and users

---

**BuildSmart** - Building the future of construction technology, one project at a time.
