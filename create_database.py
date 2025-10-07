"""
Script to create the MySQL database for the Fitness Studio API.
Run this before running migrations.
"""

import pymysql
import sys

# Database configuration
DB_HOST = 'localhost'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = 'Intothenight378#'  # Change this if your password is different
DB_NAME = 'fitness_studio_db'

def create_database():
    """Create the MySQL database if it doesn't exist."""
    try:
        print("=" * 50)
        print("Creating MySQL Database")
        print("=" * 50)
        print()
        
        # Connect to MySQL server (without specifying database)
        print(f"Connecting to MySQL server at {DB_HOST}:{DB_PORT}...")
        connection = pymysql.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            charset='utf8mb4'
        )
        
        print("Connected successfully!")
        print()
        
        # Create database
        cursor = connection.cursor()
        
        print(f"Creating database '{DB_NAME}'...")
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME} "
            f"CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        
        print(f"Database '{DB_NAME}' created successfully!")
        print()
        
        # Verify database exists
        cursor.execute("SHOW DATABASES LIKE %s", (DB_NAME,))
        result = cursor.fetchone()
        
        if result:
            print(f"✓ Verified: Database '{DB_NAME}' exists")
        else:
            print(f"✗ Warning: Could not verify database creation")
        
        cursor.close()
        connection.close()
        
        print()
        print("=" * 50)
        print("SUCCESS!")
        print("=" * 50)
        print()
        print("Next steps:")
        print("1. Run: python manage.py makemigrations")
        print("2. Run: python manage.py migrate")
        print("3. Run: python manage.py init_muscles")
        print("4. Run: python manage.py runserver")
        print()
        
        return True
        
    except pymysql.err.OperationalError as e:
        print()
        print("=" * 50)
        print("ERROR: Could not connect to MySQL")
        print("=" * 50)
        print()
        print(f"Error details: {e}")
        print()
        print("Possible solutions:")
        print("1. Make sure MySQL is running")
        print("   - Windows: Check Services → MySQL")
        print("   - Or run: net start MySQL80")
        print()
        print("2. Check your MySQL password")
        print(f"   - Current password in script: {DB_PASSWORD}")
        print(f"   - Edit this file if password is different")
        print()
        print("3. Verify MySQL is on port 3306")
        print("   - Run: netstat -an | findstr 3306")
        print()
        return False
        
    except Exception as e:
        print()
        print("=" * 50)
        print("ERROR: Unexpected error")
        print("=" * 50)
        print()
        print(f"Error: {e}")
        print()
        return False


if __name__ == "__main__":
    success = create_database()
    sys.exit(0 if success else 1)
