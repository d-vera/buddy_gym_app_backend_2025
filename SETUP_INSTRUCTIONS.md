# Complete Setup Instructions

Follow these steps to get your Fitness Studio Backend API running.

## ⚡ Quick Setup (Recommended)

### For Windows Users:

1. **Run the automated setup script**:
   ```bash
   setup.bat
   ```

2. **Create MySQL database**:
   ```sql
   CREATE DATABASE fitness_studio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

4. **Initialize muscle groups**:
   ```bash
   python manage.py init_muscles
   ```

5. **Start the server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the API**:
   - API Base: http://localhost:8000/api/
   - Swagger Docs: http://localhost:8000/api/docs/
   - Admin Panel: http://localhost:8000/admin/

---

## 📋 Manual Setup (All Platforms)

### Step 1: Verify Prerequisites

Check that you have the required software:

```bash
# Check Python version (need 3.8+)
python --version

# Check MySQL is installed
mysql --version

# Check pip is available
pip --version
```

### Step 2: Create Virtual Environment

```bash
# Navigate to project directory
cd buddy_gym_app_backend_2025

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# You should see (venv) in your terminal prompt
```

### Step 3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt
```

**Expected packages**:
- Django==4.2.7
- djangorestframework==3.14.0
- mysqlclient==2.2.0
- django-cors-headers==4.3.0
- drf-spectacular==0.26.5
- PyJWT==2.8.0
- python-dotenv==1.0.0

### Step 4: Configure MySQL Database

#### Option A: Using MySQL Command Line

```bash
# Login to MySQL
mysql -u root -p

# Enter your MySQL password when prompted
# Then run:
CREATE DATABASE fitness_studio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

#### Option B: Using MySQL Workbench

1. Open MySQL Workbench
2. Connect to your local MySQL server
3. Click "Create a new schema" button
4. Name: `fitness_studio_db`
5. Charset: `utf8mb4`
6. Collation: `utf8mb4_unicode_ci`
7. Click "Apply"

#### Option C: Using SQL Script

```bash
mysql -u root -p < database_setup.sql.example
```

### Step 5: Update Database Credentials (if needed)

If your MySQL credentials are different, edit `fitness_studio/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fitness_studio_db',
        'USER': 'your_mysql_username',      # Change if needed
        'PASSWORD': 'your_mysql_password',  # Change if needed
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}
```

### Step 6: Create Database Tables

```bash
# Create migration files
python manage.py makemigrations

# Apply migrations to database
python manage.py migrate
```

**Expected output**:
```
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  ...
  Applying api.0001_initial... OK
```

### Step 7: Initialize Muscle Groups

```bash
python manage.py init_muscles
```

**Expected output**:
```
Created muscle: Back
Created muscle: Biceps
Created muscle: Chest
Created muscle: Triceps
Created muscle: Shoulders
Created muscle: Abs
Created muscle: Legs
Created muscle: Glutes
Created muscle: Arms
Successfully created 9 muscle groups
```

### Step 8: Create Admin User (Optional)

```bash
python manage.py createsuperuser
```

Follow the prompts:
- Email: your_email@example.com
- Username: your_username
- First name: Your First Name
- Last name: Your Last Name
- Password: (enter a secure password)
- Password (again): (confirm password)

### Step 9: Start Development Server

```bash
python manage.py runserver
```

**Expected output**:
```
Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 07, 2025 - 17:00:00
Django version 4.2.7, using settings 'fitness_studio.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Step 10: Verify Installation

Open your browser and visit:

1. **API Root**: http://localhost:8000/api/
2. **Swagger Documentation**: http://localhost:8000/api/docs/
3. **Admin Panel**: http://localhost:8000/admin/ (login with superuser credentials)

---

## 🧪 Test the Installation

### Quick Test via Browser

1. Go to http://localhost:8000/api/docs/
2. You should see the Swagger UI interface
3. Try the `/api/muscles/` endpoint (requires authentication first)

### Quick Test via curl

**Register a test user**:
```bash
curl -X POST http://localhost:8000/api/auth/register/ -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"TestPass123\",\"username\":\"testuser\",\"first_name\":\"Test\",\"last_name\":\"User\"}"
```

**Login**:
```bash
curl -X POST http://localhost:8000/api/auth/login/ -H "Content-Type: application/json" -d "{\"email\":\"test@example.com\",\"password\":\"TestPass123\"}"
```

Save the token from the response and use it:

**Get muscles**:
```bash
curl -X GET http://localhost:8000/api/muscles/ -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

---

## 🔧 Troubleshooting

### Problem: "No module named 'MySQLdb'"

**Solution 1** (Windows):
```bash
pip uninstall mysqlclient
pip install mysqlclient
```

**Solution 2** (If above fails):
```bash
pip install pymysql
```

Then add to `fitness_studio/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### Problem: "Access denied for user 'root'@'localhost'"

**Solution**: Update password in `fitness_studio/settings.py` line 76-77:
```python
'USER': 'root',
'PASSWORD': 'your_actual_mysql_password',
```

### Problem: "Can't connect to MySQL server on 'localhost'"

**Solutions**:
1. Ensure MySQL service is running:
   - Windows: Check Services → MySQL
   - macOS: `brew services start mysql`
   - Linux: `sudo systemctl start mysql`

2. Verify MySQL port (default 3306):
   ```bash
   netstat -an | findstr 3306
   ```

3. Check MySQL is listening:
   ```bash
   mysql -u root -p -h localhost
   ```

### Problem: "django.db.utils.OperationalError: (1049, "Unknown database 'fitness_studio_db'")"

**Solution**: Create the database:
```sql
CREATE DATABASE fitness_studio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### Problem: Virtual environment not activating

**Windows**:
```bash
# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try again:
venv\Scripts\activate
```

**macOS/Linux**:
```bash
# Make sure you're using source:
source venv/bin/activate
```

### Problem: "Port 8000 is already in use"

**Solution**: Kill the process or use a different port:
```bash
# Use different port:
python manage.py runserver 8001

# Or find and kill the process using port 8000:
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux:
lsof -ti:8000 | xargs kill -9
```

### Problem: Migrations not applying

**Solution**:
```bash
# Delete migration files (keep __init__.py)
# Then recreate:
python manage.py makemigrations api
python manage.py migrate
```

---

## 📚 Next Steps

After successful setup:

1. **Read the documentation**:
   - `README.md` - Complete project documentation
   - `QUICKSTART.md` - Quick reference guide
   - `API_TESTING_GUIDE.md` - Comprehensive testing guide
   - `PROJECT_STRUCTURE.md` - Project architecture

2. **Test the API**:
   - Use Swagger UI: http://localhost:8000/api/docs/
   - Import Postman collection: `Fitness_Studio_API.postman_collection.json`
   - Follow `API_TESTING_GUIDE.md`

3. **Explore the Admin Panel**:
   - Visit: http://localhost:8000/admin/
   - Login with superuser credentials
   - View and manage users, exercises, trainings

4. **Start Development**:
   - Create your frontend application
   - Connect to the API endpoints
   - Implement user authentication with JWT tokens

---

## 🎯 Verification Checklist

Before considering setup complete, verify:

- [ ] Virtual environment is activated
- [ ] All dependencies installed without errors
- [ ] MySQL database `fitness_studio_db` exists
- [ ] Migrations applied successfully
- [ ] 9 muscle groups initialized
- [ ] Server starts without errors
- [ ] Swagger UI accessible at `/api/docs/`
- [ ] Can register a new user
- [ ] Can login and receive JWT token
- [ ] Can access protected endpoints with token
- [ ] Admin panel accessible (if superuser created)

---

## 🚀 Production Deployment Notes

When deploying to production:

1. **Change SECRET_KEY** in `settings.py`
2. **Set DEBUG = False**
3. **Configure ALLOWED_HOSTS**
4. **Use environment variables** for sensitive data
5. **Set up proper CORS** configuration
6. **Use production database** credentials
7. **Configure static files** serving
8. **Set up HTTPS**
9. **Implement rate limiting**
10. **Add monitoring and logging**

---

## 📞 Support

If you encounter issues not covered here:

1. Check `README.md` Troubleshooting section
2. Review Django documentation: https://docs.djangoproject.com/
3. Review DRF documentation: https://www.django-rest-framework.org/
4. Check MySQL documentation: https://dev.mysql.com/doc/

---

## ✅ Setup Complete!

Your Fitness Studio Backend API is now ready to use!

**API Base URL**: http://localhost:8000/api/
**Documentation**: http://localhost:8000/api/docs/
**Admin Panel**: http://localhost:8000/admin/

Happy coding! 🎉
