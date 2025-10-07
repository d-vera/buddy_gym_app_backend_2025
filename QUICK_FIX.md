# Quick Fix: "Unknown database 'fitness_studio_db'"

## The Problem

You're getting this error:
```
django.db.utils.OperationalError: (1049, "Unknown database 'fitness_studio_db'")
```

**Reason**: The MySQL database doesn't exist yet. You need to create it before running migrations.

## Quick Solution (Choose One)

### Option 1: Use Python Script (Recommended)

```cmd
python create_database.py
```

This will:
- Connect to MySQL
- Create the database automatically
- Verify it was created

Then run:
```cmd
python manage.py migrate
python manage.py init_muscles
python manage.py runserver
```

### Option 2: Use Batch Script

```cmd
create_database.bat
```

Enter your MySQL password when prompted.

### Option 3: Use All-in-One Script

```cmd
first_run.bat
```

This does everything automatically:
1. Creates database
2. Runs migrations
3. Initializes muscles
4. Starts server

### Option 4: Manual MySQL

1. Open **MySQL Command Line Client** or **MySQL Workbench**
2. Login with your password
3. Run this SQL command:

```sql
CREATE DATABASE fitness_studio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

4. Exit MySQL
5. Run migrations:

```cmd
python manage.py migrate
```

## Complete First-Time Setup

If this is your first time setting up:

```cmd
# 1. Run setup (if not done already)
setup.bat

# 2. Activate virtual environment (if not already active)
venv\Scripts\activate

# 3. Create database
python create_database.py

# 4. Run migrations
python manage.py makemigrations
python manage.py migrate

# 5. Initialize muscles
python manage.py init_muscles

# 6. Start server
python manage.py runserver
```

## Verify Database Was Created

After creating the database, verify it exists:

```cmd
mysql -u root -p -e "SHOW DATABASES LIKE 'fitness_studio_db';"
```

You should see:
```
+---------------------------+
| Database (fitness_studio_db) |
+---------------------------+
| fitness_studio_db         |
+---------------------------+
```

## Common Issues

### MySQL Not Running

**Error**: `Can't connect to MySQL server`

**Solution**:
```cmd
net start MySQL80
```

Or check Services → MySQL → Start

### Wrong Password

**Error**: `Access denied for user 'root'@'localhost'`

**Solution**: Edit `create_database.py` line 13:
```python
DB_PASSWORD = 'your_actual_password'
```

Or edit `fitness_studio/settings.py` line 76:
```python
'PASSWORD': 'your_actual_password',
```

### MySQL Not in PATH

**Error**: `'mysql' is not recognized`

**Solution**: Use the Python script instead:
```cmd
python create_database.py
```

## After Database is Created

Once the database exists, you can run:

```cmd
python manage.py migrate
python manage.py init_muscles
python manage.py runserver
```

Then access:
- **Swagger UI**: http://localhost:8000/api/docs/
- **API**: http://localhost:8000/api/

## Need More Help?

Check these files:
- `WINDOWS_SETUP.md` - Windows-specific guide
- `SETUP_INSTRUCTIONS.md` - Detailed setup
- `README.md` - Complete documentation
