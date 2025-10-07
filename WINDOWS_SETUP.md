# Windows Setup Guide

This guide is specifically for Windows users to set up the Fitness Studio Backend API.

## ✅ Fixed: No Visual C++ Build Tools Required!

The project now uses **PyMySQL** instead of `mysqlclient`, which means:
- ✅ No need to install Microsoft Visual C++ Build Tools
- ✅ No compilation required
- ✅ Pure Python installation

## Quick Setup Steps

### 1. Run the Setup Script

Simply double-click `setup.bat` or run in PowerShell/CMD:

```cmd
setup.bat
```

This will:
- Create a virtual environment
- Activate it
- Upgrade pip
- Install all dependencies (including PyMySQL)

### 2. Create MySQL Database

Open MySQL Command Line Client or MySQL Workbench and run:

```sql
CREATE DATABASE fitness_studio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 3. Run Database Migrations

In the **same terminal** where setup.bat ran (virtual environment is already active):

```cmd
python manage.py makemigrations
python manage.py migrate
```

### 4. Initialize Muscle Groups

```cmd
python manage.py init_muscles
```

### 5. Start the Server

```cmd
python manage.py runserver
```

### 6. Access the API

Open your browser:
- **Swagger UI**: http://localhost:8000/api/docs/
- **API Root**: http://localhost:8000/api/

## Manual Setup (If setup.bat fails)

### Step 1: Create Virtual Environment

```cmd
python -m venv venv
```

### Step 2: Activate Virtual Environment

```cmd
venv\Scripts\activate
```

You should see `(venv)` at the start of your command prompt.

### Step 3: Upgrade pip

```cmd
python -m pip install --upgrade pip
```

### Step 4: Install Dependencies

```cmd
pip install -r requirements.txt
```

All packages should install without errors now!

### Step 5: Continue with database setup (steps 2-6 above)

## Common Windows Issues & Solutions

### Issue: "python is not recognized"

**Solution**: Add Python to PATH
1. Search for "Environment Variables" in Windows
2. Click "Environment Variables"
3. Under "System variables", find "Path"
4. Add Python installation directory (e.g., `C:\Python313\`)
5. Add Scripts directory (e.g., `C:\Python313\Scripts\`)
6. Restart terminal

### Issue: "Execution Policy" error when activating venv

**Solution**: Run PowerShell as Administrator and execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```cmd
venv\Scripts\activate
```

### Issue: MySQL not running

**Solution**: Start MySQL service
1. Press `Win + R`
2. Type `services.msc`
3. Find "MySQL" or "MySQL80"
4. Right-click → Start

Or via command line (as Administrator):
```cmd
net start MySQL80
```

### Issue: Can't connect to MySQL

**Solution**: Check MySQL credentials in `fitness_studio/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fitness_studio_db',
        'USER': 'root',
        'PASSWORD': 'Intothenight378#',  # Change to your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### Issue: Port 8000 already in use

**Solution**: Find and kill the process:

```cmd
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

Or use a different port:
```cmd
python manage.py runserver 8001
```

## Verifying Installation

After setup, verify everything works:

### 1. Check Virtual Environment

```cmd
where python
```

Should show path inside `venv` folder.

### 2. Check Installed Packages

```cmd
pip list
```

Should include:
- Django (4.2.7)
- djangorestframework (3.14.0)
- pymysql (1.1.0)
- PyJWT (2.8.0)
- drf-spectacular (0.26.5)

### 3. Check Database Connection

```cmd
python manage.py dbshell
```

Should connect to MySQL. Type `exit` to quit.

### 4. Check Server

```cmd
python manage.py runserver
```

Should start without errors.

## Testing the API

### Using PowerShell

**Register a user**:
```powershell
$body = @{
    email = "test@example.com"
    password = "TestPass123"
    username = "testuser"
    first_name = "Test"
    last_name = "User"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/register/" -Method Post -Body $body -ContentType "application/json"
```

**Login**:
```powershell
$body = @{
    email = "test@example.com"
    password = "TestPass123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method Post -Body $body -ContentType "application/json"
$token = $response.token
```

**Get muscles**:
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Uri "http://localhost:8000/api/muscles/" -Method Get -Headers $headers
```

### Using Swagger UI (Recommended)

1. Go to http://localhost:8000/api/docs/
2. Click "Authorize" button
3. Enter: `Bearer YOUR_TOKEN`
4. Test all endpoints interactively

## Next Steps

1. ✅ Read `README.md` for complete documentation
2. ✅ Check `API_TESTING_GUIDE.md` for testing examples
3. ✅ Import `Fitness_Studio_API.postman_collection.json` into Postman
4. ✅ Create a superuser: `python manage.py createsuperuser`
5. ✅ Access admin panel: http://localhost:8000/admin/

## Need Help?

- Check `SETUP_INSTRUCTIONS.md` for detailed setup
- Check `QUICKSTART.md` for quick reference
- Check `README.md` for troubleshooting

## Summary of Changes

**What was fixed**:
- ❌ Removed: `mysqlclient` (requires Visual C++ Build Tools)
- ✅ Added: `pymysql` (pure Python, no compilation)
- ✅ Added: `cryptography` (for secure MySQL connections)
- ✅ Updated: `fitness_studio/__init__.py` to use PyMySQL

**Result**: Installation now works on Windows without any C++ compiler! 🎉
