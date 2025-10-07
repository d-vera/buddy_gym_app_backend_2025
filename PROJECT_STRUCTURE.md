# Project Structure

This document describes the complete structure of the Fitness Studio Backend API project.

## Directory Tree

```
buddy_gym_app_backend_2025/
│
├── fitness_studio/              # Main Django project directory
│   ├── __init__.py
│   ├── settings.py             # Project settings and configuration
│   ├── urls.py                 # Main URL routing
│   ├── asgi.py                 # ASGI configuration
│   └── wsgi.py                 # WSGI configuration
│
├── api/                        # Main API application
│   ├── __init__.py
│   ├── admin.py               # Django admin configuration
│   ├── apps.py                # App configuration
│   ├── models.py              # Database models (User, Muscle, Exercise, Training)
│   ├── serializers.py         # DRF serializers for API
│   ├── views.py               # API views and endpoints
│   ├── urls.py                # API URL routing
│   ├── authentication.py      # JWT authentication logic
│   │
│   ├── migrations/            # Database migrations
│   │   └── __init__.py
│   │
│   └── management/            # Custom management commands
│       ├── __init__.py
│       └── commands/
│           ├── __init__.py
│           └── init_muscles.py  # Command to initialize muscle groups
│
├── venv/                      # Virtual environment (created after setup)
│
├── manage.py                  # Django management script
├── requirements.txt           # Python dependencies
├── setup.bat                  # Windows setup script
├── .gitignore                # Git ignore rules
├── .env.example              # Environment variables template
├── database_setup.sql.example # SQL script for database creation
│
├── README.md                 # Comprehensive documentation
├── QUICKSTART.md            # Quick start guide
├── PROJECT_STRUCTURE.md     # This file
└── Fitness_Studio_API.postman_collection.json  # Postman collection for testing
```

## Key Files Description

### Configuration Files

- **`fitness_studio/settings.py`**: Main Django settings including database configuration, installed apps, middleware, REST framework settings, and JWT configuration.

- **`fitness_studio/urls.py`**: Root URL configuration that includes API routes and OpenAPI documentation endpoints.

- **`requirements.txt`**: Lists all Python package dependencies with versions.

- **`.env.example`**: Template for environment variables (database credentials, secret keys).

### Application Files

#### Models (`api/models.py`)
Defines four main database models:

1. **User**: Custom user model with email authentication
   - Fields: email, username (nickname), first_name, last_name, password
   - Extends AbstractBaseUser for custom authentication

2. **Muscle**: Predefined muscle groups
   - Fields: name (choices: back, biceps, chest, triceps, shoulders, abs, legs, glutes, arms)

3. **Exercise**: User-created exercises
   - Fields: user, muscle, name, note, created_at, updated_at
   - Each user can create custom exercises for each muscle

4. **Training**: Training session records
   - Fields: user, exercise, weight, sets, repetitions, datetime
   - Tracks individual workout sessions

#### Serializers (`api/serializers.py`)
DRF serializers for data validation and transformation:

- **UserRegistrationSerializer**: Validates user registration with email/nickname uniqueness and password strength
- **UserLoginSerializer**: Validates login credentials
- **UserSerializer**: User profile data
- **MuscleSerializer**: Muscle group data
- **ExerciseSerializer**: Exercise CRUD operations
- **TrainingSerializer**: Training session data
- **TrainingStatsSerializer**: Training statistics aggregation

#### Views (`api/views.py`)
API endpoints implementation:

**Function-based views:**
- `register()`: User registration
- `login()`: User authentication and JWT token generation
- `profile()`: Get current user profile

**Class-based viewsets:**
- `MuscleViewSet`: Read-only muscle group endpoints
- `ExerciseViewSet`: Full CRUD for exercises with muscle filtering
- `TrainingViewSet`: Full CRUD for trainings with custom actions:
  - `history()`: Filtered training history (by period, exercise, muscle)
  - `stats()`: Training statistics (low/high/last weight)

#### Authentication (`api/authentication.py`)
Custom JWT authentication:

- `generate_jwt_token()`: Creates JWT tokens for authenticated users
- `JWTAuthentication`: DRF authentication class for validating JWT tokens
- Token expiration: 24 hours
- Bearer token format: `Authorization: Bearer <token>`

#### Admin (`api/admin.py`)
Django admin panel configuration for all models with custom list displays, filters, and search capabilities.

### Management Commands

#### `init_muscles.py`
Custom Django management command to populate the database with the 9 predefined muscle groups.

Usage: `python manage.py init_muscles`

### Documentation Files

- **`README.md`**: Complete project documentation including features, installation, API endpoints, usage examples, and troubleshooting.

- **`QUICKSTART.md`**: Condensed guide for quick setup and testing.

- **`PROJECT_STRUCTURE.md`**: This file - explains the project organization.

### Testing Files

- **`Fitness_Studio_API.postman_collection.json`**: Postman collection with all API endpoints pre-configured for easy testing.

### Setup Files

- **`setup.bat`**: Automated setup script for Windows to create virtual environment and install dependencies.

- **`database_setup.sql.example`**: SQL script to create the MySQL database.

## Database Schema

### Tables Created by Django Migrations

1. **users**: Custom user table
2. **muscles**: Muscle groups lookup table
3. **exercises**: User exercises
4. **training**: Training sessions
5. Django system tables (auth, sessions, admin, etc.)

### Relationships

```
User (1) ──────< (N) Exercise
              │
              └──< (N) Training

Muscle (1) ────< (N) Exercise
                    │
                    └──< (N) Training (through Exercise)
```

## API Endpoints Structure

### Authentication (`/api/auth/`)
- `POST /register/` - Register new user
- `POST /login/` - Login and get JWT token
- `GET /profile/` - Get current user profile

### Muscles (`/api/muscles/`)
- `GET /` - List all muscles
- `GET /{id}/` - Get specific muscle

### Exercises (`/api/exercises/`)
- `GET /` - List user's exercises
- `POST /` - Create exercise
- `GET /{id}/` - Get specific exercise
- `PUT /{id}/` - Update exercise
- `PATCH /{id}/` - Partial update
- `DELETE /{id}/` - Delete exercise

### Trainings (`/api/trainings/`)
- `GET /` - List all trainings
- `POST /` - Create training
- `GET /{id}/` - Get specific training
- `PUT /{id}/` - Update training
- `PATCH /{id}/` - Partial update
- `DELETE /{id}/` - Delete training
- `GET /history/` - Get filtered history
- `GET /stats/` - Get statistics

### Documentation (`/api/`)
- `GET /schema/` - OpenAPI schema
- `GET /docs/` - Swagger UI
- `GET /redoc/` - ReDoc UI

## Technology Stack Details

### Backend Framework
- **Django 4.2.7**: Web framework
- **Django REST Framework 3.14.0**: REST API toolkit

### Database
- **MySQL**: Primary database
- **mysqlclient 2.2.0**: MySQL database adapter

### Authentication
- **PyJWT 2.8.0**: JWT token generation and validation

### Documentation
- **drf-spectacular 0.26.5**: OpenAPI 3.0 schema generation

### Additional
- **django-cors-headers 4.3.0**: CORS handling
- **python-dotenv 1.0.0**: Environment variable management

## Development Workflow

1. **Setup**: Run `setup.bat` or manual setup
2. **Database**: Create MySQL database
3. **Migrations**: `python manage.py migrate`
4. **Initialize**: `python manage.py init_muscles`
5. **Run**: `python manage.py runserver`
6. **Test**: Use Swagger UI or Postman collection
7. **Admin**: Access Django admin at `/admin/`

## Security Features

- Password hashing using Django's PBKDF2 algorithm
- JWT token-based authentication
- Password validation (min 8 characters)
- Email and username uniqueness validation
- CORS configuration
- User-specific data isolation (exercises and trainings)

## Extensibility

The project is designed for easy extension:

- Add new muscle groups in `Muscle.MUSCLE_CHOICES`
- Add new fields to models with migrations
- Create new endpoints by adding views and URL patterns
- Add custom management commands in `api/management/commands/`
- Extend serializers for additional validation
- Add custom permissions in views

## Next Steps for Development

1. Add unit tests (`api/tests.py`)
2. Add integration tests
3. Implement refresh tokens for JWT
4. Add email verification for registration
5. Add password reset functionality
6. Implement rate limiting
7. Add caching for frequently accessed data
8. Create Docker configuration
9. Add CI/CD pipeline
10. Deploy to production server
