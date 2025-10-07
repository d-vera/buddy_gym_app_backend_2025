@echo off
echo ========================================
echo Fitness Studio - First Run Setup
echo ========================================
echo.
echo This script will:
echo 1. Create the MySQL database
echo 2. Run migrations
echo 3. Initialize muscle groups
echo 4. Start the server
echo.
echo Make sure:
echo - Virtual environment is activated (run setup.bat first if not)
echo - MySQL is running
echo.
pause
echo.

REM Check if virtual environment is activated
python -c "import sys; sys.exit(0 if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) else 1)"
if %errorlevel% neq 0 (
    echo ERROR: Virtual environment is not activated!
    echo.
    echo Please run: venv\Scripts\activate
    echo Then run this script again.
    echo.
    pause
    exit /b 1
)

echo ========================================
echo Step 1: Creating Database
echo ========================================
echo.

python create_database.py
if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to create database
    echo Please fix the error above and try again.
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 2: Creating Migrations
echo ========================================
echo.

python manage.py makemigrations
if %errorlevel% neq 0 (
    echo ERROR: Failed to create migrations
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 3: Running Migrations
echo ========================================
echo.

python manage.py migrate
if %errorlevel% neq 0 (
    echo ERROR: Failed to run migrations
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 4: Initializing Muscle Groups
echo ========================================
echo.

python manage.py init_muscles
if %errorlevel% neq 0 (
    echo ERROR: Failed to initialize muscles
    pause
    exit /b 1
)

echo.
echo ========================================
echo Step 5: Creating Superuser (Optional)
echo ========================================
echo.
echo Would you like to create an admin user? (Y/N)
set /p create_admin=

if /i "%create_admin%"=="Y" (
    echo.
    python manage.py createsuperuser
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Starting development server...
echo.
echo Access the API at:
echo - Swagger UI: http://localhost:8000/api/docs/
echo - API Root:   http://localhost:8000/api/
echo - Admin:      http://localhost:8000/admin/
echo.
echo Press Ctrl+C to stop the server
echo.
pause

python manage.py runserver
