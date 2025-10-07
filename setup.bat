@echo off
echo ========================================
echo Fitness Studio Backend Setup
echo ========================================
echo.

echo Step 1: Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)
echo Virtual environment created successfully!
echo.

echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)
echo Virtual environment activated!
echo.

echo Step 3: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 4: Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    echo.
    echo If you see errors, try running this manually:
    echo   venv\Scripts\activate
    echo   pip install -r requirements.txt
    pause
    exit /b 1
)
echo Dependencies installed successfully!
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Make sure MySQL is running
echo 2. Create database: CREATE DATABASE fitness_studio_db;
echo 3. Keep this terminal open and run:
echo    python manage.py makemigrations
echo    python manage.py migrate
echo    python manage.py init_muscles
echo    python manage.py runserver
echo.
echo Note: Virtual environment is already activated in this window!
echo.
pause
