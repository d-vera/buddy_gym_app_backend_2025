# Fitness Studio Backend API

A comprehensive Django REST API backend for managing a fitness studio application. This API allows users to register, manage exercises, track training sessions, and view training history and statistics.

## Features

- **User Management**
  - User registration with email, password, first name, last name, and unique nickname
  - Email and nickname uniqueness validation
  - Password validation (minimum 8 characters)
  - JWT-based authentication
  - User login and profile management

- **Muscle Groups**
  - Predefined muscle groups: back, biceps, chest, triceps, shoulders, abs, legs, glutes, arms
  - List all available muscle groups

- **Exercise Management**
  - Create, read, update, and delete exercises for each muscle group
  - Each exercise includes a name and optional note
  - Exercises are user-specific
  - Filter exercises by muscle group

- **Training Sessions**
  - Register training sessions with weight, sets, and repetitions
  - Automatic datetime tracking
  - View complete training history
  - Filter history by time periods: current week, last week, last month, last year
  - Filter by exercise or muscle group

- **Training Statistics**
  - View low weight, high weight, and last weight for each exercise
  - Total session count per exercise
  - Filter statistics by exercise or muscle
- **API Documentation**
  - Interactive Swagger UI documentation
  - ReDoc documentation
  - OpenAPI 3.0 schema

## Technology Stack

- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Database**: MySQL (using PyMySQL adapter)
- **Authentication**: JWT (PyJWT)
- **Documentation**: drf-spectacular (OpenAPI/Swagger)
- **CORS**: django-cors-headers

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd buddy_gym_app_backend_2025
```

### 2. Create a virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL Database

Make sure MySQL is running and create the database:

```sql
CREATE DATABASE fitness_studio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

The database connection is already configured in `fitness_studio/settings.py`:
- Server: localhost
- Port: 3306
- User: root
- Password: Intothenight378#
- Database: fitness_studio_db

### 5. Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Initialize muscle groups

```bash
python manage.py init_muscles
```

### 7. Create a superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 8. Run the development server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000/`

## API Documentation

Once the server is running, you can access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

## API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register a new user | No |
| POST | `/api/auth/login/` | Login and get JWT token | No |
| GET | `/api/auth/profile/` | Get current user profile | Yes |

### Muscles

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/muscles/` | List all muscle groups | Yes |
| GET | `/api/muscles/{id}/` | Get specific muscle group | Yes |

### Exercises

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/exercises/` | List user's exercises | Yes |
| POST | `/api/exercises/` | Create new exercise | Yes |
| GET | `/api/exercises/{id}/` | Get specific exercise | Yes |
| PUT | `/api/exercises/{id}/` | Update exercise | Yes |
| PATCH | `/api/exercises/{id}/` | Partial update exercise | Yes |
| DELETE | `/api/exercises/{id}/` | Delete exercise | Yes |

### Training Sessions

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/trainings/` | List all training sessions | Yes |
| POST | `/api/trainings/` | Create new training session | Yes |
| GET | `/api/trainings/{id}/` | Get specific training session | Yes |
| PUT | `/api/trainings/{id}/` | Update training session | Yes |
| PATCH | `/api/trainings/{id}/` | Partial update training | Yes |
| DELETE | `/api/trainings/{id}/` | Delete training session | Yes |
| GET | `/api/trainings/history/` | Get filtered training history | Yes |
| GET | `/api/trainings/stats/` | Get training statistics | Yes |

## Usage Examples

### 1. Register a new user

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe"
  }'
```

### 2. Login

You can login with either **email** or **username (nickname)**:

**Login with email:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_username": "john@example.com",
    "password": "SecurePass123"
  }'
```

**Login with username:**
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email_or_username": "johndoe",
    "password": "SecurePass123"
  }'
```

Response:
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe"
  },
  "message": "Login successful"
}
```

### 3. Create an exercise

```bash
curl -X POST http://localhost:8000/api/exercises/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "muscle": 1,
    "name": "Bench Press",
    "note": "Focus on form and controlled movements"
  }'
```

### 4. Register a training session

```bash
curl -X POST http://localhost:8000/api/trainings/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "exercise": 1,
    "weight": 80.5,
    "sets": 4,
    "repetitions": 10
  }'
```

### 5. Get training history for last week

```bash
curl -X GET "http://localhost:8000/api/trainings/history/?period=last_week" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### 6. Get training statistics

```bash
curl -X GET http://localhost:8000/api/trainings/stats/ \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Database Schema

### Users Table
- `id`: Primary key
- `email`: Unique email address
- `user`: Unique username/nickname
- `first_name`: User's first name
- `last_name`: User's last name
- `password`: Hashed password
- `is_active`: Boolean
- `is_staff`: Boolean
- `date_joined`: Timestamp

### Muscles Table
- `id`: Primary key
- `name`: Muscle group name (unique)

### Exercises Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `muscle_id`: Foreign key to Muscles
- `name`: Exercise name
- `note`: Exercise description/notes
- `created_at`: Timestamp
- `updated_at`: Timestamp

### Training Table
- `id`: Primary key
- `user_id`: Foreign key to Users
- `exercise_id`: Foreign key to Exercises
- `weight`: Decimal (weight used)
- `sets`: Integer (number of sets)
- `repetitions`: Integer (number of repetitions)
- `datetime`: Timestamp (auto-generated)

## Security Notes

- **JWT Tokens**: Tokens expire after 24 hours
- **Password Validation**: Minimum 8 characters with Django's built-in validators
- **CORS**: Currently set to allow all origins (configure for production)
- **Secret Key**: Change the SECRET_KEY in settings.py for production
- **Debug Mode**: Set DEBUG=False in production

## Development

### Running Tests

```bash
python manage.py test
```

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Accessing Django Admin
Navigate to `http://localhost:8000/admin/` and login with your superuser credentials.

## Troubleshooting

### MySQL Connection Issues

If you encounter MySQL connection errors:
1. Ensure MySQL server is running
2. Verify database credentials in `settings.py`
3. Check that the database `fitness_studio_db` exists
4. PyMySQL is used as the MySQL adapter (no compilation required)

### Virtual Environment Issues

If packages aren't found:
1. Ensure virtual environment is activated

## License

This project is licensed under the MIT License.

## Support

For issues and questions, please open an issue in the repository.
