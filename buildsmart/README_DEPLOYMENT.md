# BuildSmart - Deployment Guide

## 🚀 Quick Start

### 1. Install Dependencies

```bash
cd buildsmart
pip install -r requirements.txt
```

### 2. Configure Environment

Create a `.env` file in the `buildsmart` directory:

```env
# Application
FLASK_APP=app:create_app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here

# Database
DATABASE_URL=sqlite:///buildsmart.db

# Email (Optional)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password

# Cache (Optional - uses simple cache if not set)
CACHE_TYPE=simple
# CACHE_REDIS_URL=redis://localhost:6379/0

# SMS (Optional)
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_FROM_NUMBER=your-phone-number

# Frontend URL
FRONTEND_URL=http://localhost:5000
```

### 3. Initialize Database

```bash
# Create migrations (if needed)
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade

# Seed database (optional)
python seed_database.py
```

### 4. Run Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`

---

## 📚 Access Points

### Web Interface
- **Home:** `http://localhost:5000`
- **Admin Dashboard:** `http://localhost:5000/admin/dashboard`
- **Shop Dashboard:** `http://localhost:5000/shop/dashboard`
- **User Dashboard:** `http://localhost:5000/user/dashboard`

### API Documentation
- **Swagger UI:** `http://localhost:5000/api/docs`
- **OpenAPI Spec:** `http://localhost:5000/apispec.json`

---

## 🧪 Testing

### Run All Tests

```bash
pytest tests/
```

### Run Specific Test Files

```bash
# Security tests
pytest tests/test_security.py

# Payment tests
pytest tests/test_payment_features.py

# Analytics tests
pytest tests/test_analytics_features.py

# Performance tests
pytest tests/test_performance_features.py

# Integration tests
pytest tests/test_integration.py
```

### Run with Coverage

```bash
pytest --cov=app tests/
```

---

## 🔧 Configuration

### Development

Uses SQLite database and simple in-memory cache.

### Production

1. Set `FLASK_ENV=production`
2. Configure PostgreSQL database
3. Configure Redis cache
4. Set secure `SECRET_KEY`
5. Configure email service
6. Set up reverse proxy (nginx)
7. Use WSGI server (gunicorn)

### Production Environment Variables

```env
FLASK_ENV=production
DATABASE_URL=postgresql://user:password@localhost/buildsmart
SECRET_KEY=your-production-secret-key
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://localhost:6379/0
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## 📊 Database Setup

### Create Migrations

```bash
flask db migrate -m "Description of changes"
```

### Apply Migrations

```bash
flask db upgrade
```

### Rollback Migration

```bash
flask db downgrade
```

### Index Recommendations

See `app/utils/database_indexes.py` for recommended indexes. Create indexes via migrations for optimal performance.

---

## 🔒 Security Configuration

### Required Settings
- Set strong `SECRET_KEY`
- Configure email for verification
- Enable rate limiting
- Set up HTTPS in production
- Configure CORS properly

### Optional Settings
- Configure SMS service
- Set up Redis for rate limiting
- Configure security headers

---

## ⚡ Performance Configuration

### Caching

**Development:**
- Uses simple in-memory cache (default)

**Production:**
- Configure Redis:
```env
CACHE_TYPE=redis
CACHE_REDIS_URL=redis://localhost:6379/0
```

### Database Indexes

Apply recommended indexes from `app/utils/database_indexes.py` via migrations.

---

## 📧 Email Configuration

### Gmail Setup

1. Enable 2-Step Verification
2. Generate App Password
3. Configure in `.env`:
```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=true
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

---

## 📱 SMS Configuration

### Twilio Setup

1. Create Twilio account
2. Get Account SID and Auth Token
3. Get phone number
4. Configure in `.env`:
```env
SMS_PROVIDER=twilio
TWILIO_ACCOUNT_SID=your-account-sid
TWILIO_AUTH_TOKEN=your-auth-token
TWILIO_FROM_NUMBER=+1234567890
```

### Africa's Talking Setup

1. Create Africa's Talking account
2. Get API credentials
3. Configure in `.env`:
```env
SMS_PROVIDER=africas_talking
AT_USERNAME=your-username
AT_API_KEY=your-api-key
AT_SENDER_ID=BUILDSMART
```

---

## 🐛 Troubleshooting

### Import Errors

**Issue:** `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
pip install -r requirements.txt
```

### Database Errors

**Issue:** Database connection errors

**Solution:**
1. Check `DATABASE_URL` in `.env`
2. Ensure database exists
3. Run migrations: `flask db upgrade`

### Cache Errors

**Issue:** Cache not working

**Solution:**
1. Check `CACHE_TYPE` in `.env`
2. For Redis, ensure Redis server is running
3. Application will degrade gracefully if cache fails

### Email Errors

**Issue:** Email not sending

**Solution:**
1. Check email configuration in `.env`
2. Verify SMTP credentials
3. Check firewall/network settings

---

## 📖 Documentation

- **Security:** `SECURITY_IMPLEMENTATION.md`
- **UX Features:** `UX_FEATURES_IMPLEMENTATION.md`
- **Business Logic:** `BUSINESS_LOGIC_IMPLEMENTATION.md`
- **Communication:** `COMMUNICATION_NOTIFICATIONS_IMPLEMENTATION.md`
- **Payments:** `PAYMENT_FEATURES_IMPLEMENTATION.md`
- **Analytics:** `ANALYTICS_IMPLEMENTATION.md`
- **Performance:** `PERFORMANCE_IMPLEMENTATION.md`
- **API Docs:** `API_DOCUMENTATION_IMPLEMENTATION.md`
- **Final Summary:** `FINAL_IMPLEMENTATION_SUMMARY.md`

---

## ✅ Verification

After deployment, verify:

1. ✅ Application starts without errors
2. ✅ Database migrations applied
3. ✅ All endpoints accessible
4. ✅ API documentation available
5. ✅ Security features working
6. ✅ Caching operational (if configured)
7. ✅ Email service working (if configured)

---

**Status:** ✅ Production Ready  
**Last Updated:** 2024-01-01

