# How to Run the BuildSmart Backend

## Quick Start (3 Steps)

### Step 1: Activate Virtual Environment

**Windows (PowerShell):**
```powershell
cd buildsmart
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
cd buildsmart
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
cd buildsmart
source venv/bin/activate
```

### Step 2: Initialize Database (First time only)

**Option A: Use seed script (recommended - includes sample data):**
```bash
python seed_database.py
```

**Option B: Use Flask command (basic data only):**
```bash
python -m flask db upgrade
python -m flask init-db
```

### Step 3: Run the Server

```bash
python run.py
```

The backend will start on **http://localhost:5000**

---

## Detailed Setup (If virtual environment is not set up)

### 1. Create Virtual Environment

**Windows:**
```powershell
cd buildsmart
python -m venv venv
```

**macOS/Linux:**
```bash
cd buildsmart
python3 -m venv venv
```

### 2. Activate Virtual Environment

**Windows (PowerShell):**
```powershell
.\venv\Scripts\Activate.ps1
```

**Windows (Command Prompt):**
```cmd
venv\Scripts\activate.bat
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables (Optional)

Create a `.env` file in the `buildsmart` directory:

```env
FLASK_APP=app:create_app
FLASK_ENV=development
DATABASE_URL=sqlite:///buildsmart.db
SECRET_KEY=your-secret-key-here-change-in-production
```

**Note:** The app will work without a `.env` file as it uses default values.

### 5. Initialize Database

```bash
# Run migrations first
python -m flask db upgrade

# Then seed with sample data (recommended)
python seed_database.py
```

### 6. Run the Server

```bash
python run.py
```

---

## Verify Backend is Running

1. Open your browser and go to: **http://localhost:5000**
2. You should see the BuildSmart homepage
3. Check API endpoints:
   - **http://localhost:5000/api/categories** - Should return categories
   - **http://localhost:5000/api/products/search?q=cement** - Should return products

---

## Troubleshooting

### Virtual Environment Issues

**If activation fails on Windows PowerShell:**
```powershell
# Run this first to allow scripts
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Port Already in Use

If port 5000 is already in use, you can change it in `run.py`:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)  # Change port here
```

### Database Issues

**Reset the database:**
```bash
# Delete the database file
rm buildsmart.db  # or del buildsmart.db on Windows

# Recreate and seed
python seed_database.py
```

### Missing Dependencies

If you get import errors:
```bash
# Make sure venv is activated
pip install -r requirements.txt
```

---

## Default Login Credentials (After Seeding)

**Customer:**
- Username: `john_doe`
- Email: `john@example.com`
- Password: `password123`

**Shop Owner:**
- Username: `shop_owner`
- Email: `owner@buildsmart.com`
- Password: `password123`

---

## API Endpoints for Mobile App

The Flutter mobile app expects these endpoints:
- `GET /api/categories` - Product categories
- `GET /api/products/search?q={query}` - Search products
- `GET /api/shops/nearby?lat={lat}&lon={lon}&radius={radius}` - Nearby shops
- `GET /api/services/search` - Search services
- `POST /auth/login` - User login
- `POST /auth/register` - User registration
- `GET /user/dashboard` - User dashboard (requires auth)

---

## Running in Background (Optional)

**Windows:**
```powershell
Start-Process python -ArgumentList "run.py" -WindowStyle Hidden
```

**macOS/Linux:**
```bash
nohup python run.py > server.log 2>&1 &
```

---

## Next Steps

1. ✅ Backend running on http://localhost:5000
2. ✅ Update mobile app `.env` file with backend URL:
   ```
   API_BASE_URL=http://localhost:5000
   ```
3. ✅ Test mobile app connection to backend

---

**Happy Coding! 🚀**

