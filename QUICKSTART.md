# Quick Start Guide

This guide will help you get the Fitness Studio Backend API up and running quickly.

## Prerequisites Check

Before starting, ensure you have:
- ✅ Python 3.8+ installed (`python --version`)
- ✅ MySQL Server running (`mysql --version`)
- ✅ Git installed (if cloning from repository)

## Quick Setup (5 minutes)

### Step 1: Setup Virtual Environment and Install Dependencies

**Windows:**
```bash
# Run the automated setup script
setup.bat
```

**Manual Setup (All platforms):**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Create MySQL Database

Open MySQL command line or MySQL Workbench and run:

```sql
CREATE DATABASE fitness_studio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Or use the provided SQL script:
```bash
mysql -u root -p < database_setup.sql
```

### Step 3: Run Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4: Initialize Muscle Groups

```bash
python manage.py init_muscles
```

This will create the 9 predefined muscle groups:
- back, biceps, chest, triceps, shoulders, abs, legs, glutes, arms

### Step 5: (Optional) Create Admin User

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 6: Start the Server

```bash
python manage.py runserver
```

The API is now running at: **http://localhost:8000/**

## Test the API

### Option 1: Use Swagger UI (Recommended)

Open your browser and go to:
**http://localhost:8000/api/docs/**

This provides an interactive interface to test all endpoints.

### Option 2: Use curl

**Register a user:**
```bash
curl -X POST http://localhost:8000/api/auth/register/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"TestPass123\",\"username\":\"testuser\",\"first_name\":\"Test\",\"last_name\":\"User\"}"
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email\":\"test@example.com\",\"password\":\"TestPass123\"}"
```

Copy the token from the response and use it in subsequent requests:

**Get muscles:**
```bash
curl -X GET http://localhost:8000/api/muscles/ ^
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

## Common Issues

### Issue: "No module named 'MySQLdb'"
**Solution:** Install mysqlclient
```bash
pip install mysqlclient
```

If that fails on Windows, try:
```bash
pip install pymysql
```

Then add to `fitness_studio/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Issue: "Access denied for user 'root'@'localhost'"
**Solution:** Update the password in `fitness_studio/settings.py` line 76:
```python
'PASSWORD': 'your_actual_mysql_password',
```

### Issue: "Can't connect to MySQL server"
**Solution:** 
1. Ensure MySQL is running
2. Check the port (default: 3306)
3. Verify host is 'localhost'

## Next Steps

1. **Explore the API Documentation**: http://localhost:8000/api/docs/
2. **Access Django Admin**: http://localhost:8000/admin/
3. **Read the full README.md** for detailed API documentation
4. **Start building your frontend** using the API endpoints

## API Endpoints Summary

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register/` | POST | Register new user |
| `/api/auth/login/` | POST | Login and get token |
| `/api/auth/profile/` | GET | Get user profile |
| `/api/muscles/` | GET | List muscle groups |
| `/api/exercises/` | GET/POST | Manage exercises |
| `/api/trainings/` | GET/POST | Manage trainings |
| `/api/trainings/history/` | GET | Get training history |
| `/api/trainings/stats/` | GET | Get training statistics |

## Support

For detailed documentation, see **README.md**

For issues, check the Troubleshooting section in README.md
