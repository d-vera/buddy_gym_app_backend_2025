@echo off
echo ========================================
echo Creating MySQL Database
echo ========================================
echo.

echo This script will create the fitness_studio_db database.
echo.
echo Please enter your MySQL root password when prompted.
echo.

mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS fitness_studio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Failed to create database
    echo.
    echo Possible issues:
    echo 1. MySQL is not running
    echo 2. Incorrect password
    echo 3. MySQL is not in your PATH
    echo.
    echo Try manually:
    echo 1. Open MySQL Command Line Client
    echo 2. Enter your password
    echo 3. Run: CREATE DATABASE fitness_studio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo Database created successfully!
echo ========================================
echo.
echo You can now run:
echo   python manage.py migrate
echo.
pause
