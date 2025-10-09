# Changelog

All notable changes to the Fitness Studio Backend API.

## [1.1.0] - 2025-10-09

### Added
- **Flexible Login**: Users can now login with either email or username (nickname)
- Enhanced OpenAPI documentation with request examples for login endpoint
- Better error messages for authentication failures

### Changed
- **Login endpoint** (`POST /api/auth/login/`)
  - Field changed from `email` to `email_or_username`
  - Now accepts both email addresses and usernames
  - Updated response to include descriptive error messages
  
### Updated Documentation
- `README.md` - Updated login examples to show both email and username login
- `API_TESTING_GUIDE.md` - Added examples for both login methods
- `Fitness_Studio_API.postman_collection.json` - Added separate requests for email and username login
- OpenAPI schema now includes request examples for both login methods

### Technical Details
- Modified `UserLoginSerializer` to accept `email_or_username` field
- Updated `login` view to detect whether input is email (contains '@') or username
- Added OpenAPI examples using `drf_spectacular.utils.OpenApiExample`

---

## [1.0.0] - 2025-10-07

### Initial Release

#### Features
- User registration with email, password, first name, last name, and unique username
- JWT-based authentication
- User login and profile management
- 9 predefined muscle groups (back, biceps, chest, triceps, shoulders, abs, legs, glutes, arms)
- Exercise management (CRUD operations)
- Training session tracking with weight, sets, and repetitions
- Training history with time-based filtering (current week, last week, last month, last year)
- Training statistics (low weight, high weight, last weight)
- OpenAPI/Swagger documentation
- MySQL database integration using PyMySQL
- CORS support
- Django admin panel

#### API Endpoints
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `GET /api/auth/profile/` - Get user profile
- `GET /api/muscles/` - List muscle groups
- `GET /api/exercises/` - List exercises
- `POST /api/exercises/` - Create exercise
- `GET/PUT/PATCH/DELETE /api/exercises/{id}/` - Exercise operations
- `GET /api/trainings/` - List trainings
- `POST /api/trainings/` - Create training
- `GET/PUT/PATCH/DELETE /api/trainings/{id}/` - Training operations
- `GET /api/trainings/history/` - Training history with filters
- `GET /api/trainings/stats/` - Training statistics

#### Database
- MySQL database with PyMySQL adapter (no compilation required)
- Custom User model with email as USERNAME_FIELD
- Muscle, Exercise, and Training models
- Proper foreign key relationships

#### Documentation
- Comprehensive README.md
- Quick start guide (QUICKSTART.md)
- Windows setup guide (WINDOWS_SETUP.md)
- API testing guide (API_TESTING_GUIDE.md)
- Project structure documentation (PROJECT_STRUCTURE.md)
- Postman collection for API testing
- Interactive Swagger UI
- ReDoc documentation

#### Setup Scripts
- `setup.bat` - Automated Windows setup
- `create_database.py` - Database creation script
- `create_database.bat` - Windows batch database creation
- `first_run.bat` - Complete first-time setup automation

---

## Migration Guide

### Upgrading from 1.0.0 to 1.1.0

If you have existing code that uses the login endpoint, update your requests:

**Before (v1.0.0):**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**After (v1.1.0):**
```json
{
  "email_or_username": "user@example.com",
  "password": "password123"
}
```

Or use username:
```json
{
  "email_or_username": "username",
  "password": "password123"
}
```

**No database migrations required** - this is a backward-compatible API change.

---

## Future Enhancements

Planned features for future releases:
- [ ] Refresh token support
- [ ] Email verification for registration
- [ ] Password reset functionality
- [ ] Rate limiting
- [ ] Caching for frequently accessed data
- [ ] Docker support
- [ ] Unit and integration tests
- [ ] CI/CD pipeline
- [ ] File upload for exercise images
- [ ] Social authentication (Google, Facebook)
- [ ] Workout plans and routines
- [ ] Progress tracking and analytics
- [ ] Export training data (CSV, PDF)
