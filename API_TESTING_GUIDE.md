# API Testing Guide

This guide provides step-by-step instructions for testing all API endpoints of the Fitness Studio Backend.

## Prerequisites

1. Server is running: `python manage.py runserver`
2. Database is set up and migrated
3. Muscle groups are initialized: `python manage.py init_muscles`

## Testing Methods

You can test the API using:
1. **Swagger UI** (Recommended): http://localhost:8000/api/docs/
2. **Postman**: Import `Fitness_Studio_API.postman_collection.json`
3. **curl** commands (examples below)
4. **Python requests** library

## Complete Testing Workflow

### Step 1: Register a New User

**Endpoint**: `POST /api/auth/register/`

**Request**:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"TestPass123\",\"username\":\"testuser\",\"first_name\":\"Test\",\"last_name\":\"User\"}"
```

**Expected Response** (201 Created):
```json
{
  "user": {
    "id": 1,
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "date_joined": "2025-10-07T21:00:00Z"
  },
  "message": "User registered successfully"
}
```

**Validation Tests**:

❌ **Duplicate Email**:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"test@example.com\",\"password\":\"TestPass123\",\"username\":\"newuser\",\"first_name\":\"New\",\"last_name\":\"User\"}"
```
Expected: 400 Bad Request - "A user with this email already exists."

❌ **Duplicate Username**:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"new@example.com\",\"password\":\"TestPass123\",\"username\":\"testuser\",\"first_name\":\"New\",\"last_name\":\"User\"}"
```
Expected: 400 Bad Request - "A user with this nickname already exists."

❌ **Short Password**:
```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d "{\"email\":\"new@example.com\",\"password\":\"short\",\"username\":\"newuser\",\"first_name\":\"New\",\"last_name\":\"User\"}"
```
Expected: 400 Bad Request - "Password must be at least 8 characters long."

### Step 2: Login

**Endpoint**: `POST /api/auth/login/`

You can login with either **email** or **username (nickname)**.

**Request (with email)**:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email_or_username\":\"test@example.com\",\"password\":\"TestPass123\"}"
```

**Request (with username)**:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email_or_username\":\"testuser\",\"password\":\"TestPass123\"}"
```

**Expected Response** (200 OK):
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "user": {
    "id": 1,
    "email": "test@example.com",
    "username": "testuser",
    "first_name": "Test",
    "last_name": "User",
    "date_joined": "2025-10-07T21:00:00Z"
  },
  "message": "Login successful"
}
```

**Save the token** for subsequent requests!

❌ **Invalid Credentials**:
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d "{\"email_or_username\":\"test@example.com\",\"password\":\"WrongPass\"}"
```
Expected: 401 Unauthorized - "Invalid credentials. Please check your email/username and password."

### Step 3: Get User Profile

**Endpoint**: `GET /api/auth/profile/`

**Request**:
```bash
curl -X GET http://localhost:8000/api/auth/profile/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response** (200 OK):
```json
{
  "id": 1,
  "email": "test@example.com",
  "username": "testuser",
  "first_name": "Test",
  "last_name": "User",
  "date_joined": "2025-10-07T21:00:00Z"
}
```

### Step 4: List Muscle Groups

**Endpoint**: `GET /api/muscles/`

**Request**:
```bash
curl -X GET http://localhost:8000/api/muscles/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response** (200 OK):
```json
[
  {"id": 1, "name": "back"},
  {"id": 2, "name": "biceps"},
  {"id": 3, "name": "chest"},
  {"id": 4, "name": "triceps"},
  {"id": 5, "name": "shoulders"},
  {"id": 6, "name": "abs"},
  {"id": 7, "name": "legs"},
  {"id": 8, "name": "glutes"},
  {"id": 9, "name": "arms"}
]
```

### Step 5: Create Exercises

**Endpoint**: `POST /api/exercises/`

**Create Exercise 1 - Bench Press (Chest)**:
```bash
curl -X POST http://localhost:8000/api/exercises/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"muscle\":3,\"name\":\"Bench Press\",\"note\":\"Focus on form and controlled movements\"}"
```

**Create Exercise 2 - Squats (Legs)**:
```bash
curl -X POST http://localhost:8000/api/exercises/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"muscle\":7,\"name\":\"Squats\",\"note\":\"Keep back straight, go deep\"}"
```

**Create Exercise 3 - Deadlift (Back)**:
```bash
curl -X POST http://localhost:8000/api/exercises/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"muscle\":1,\"name\":\"Deadlift\",\"note\":\"Engage core, lift with legs\"}"
```

**Expected Response** (201 Created):
```json
{
  "id": 1,
  "muscle": 3,
  "muscle_name": "chest",
  "name": "Bench Press",
  "note": "Focus on form and controlled movements",
  "created_at": "2025-10-07T21:05:00Z",
  "updated_at": "2025-10-07T21:05:00Z"
}
```

### Step 6: List All Exercises

**Endpoint**: `GET /api/exercises/`

**Request**:
```bash
curl -X GET http://localhost:8000/api/exercises/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Filter by Muscle** (e.g., chest exercises):
```bash
curl -X GET "http://localhost:8000/api/exercises/?muscle=3" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Step 7: Update an Exercise

**Endpoint**: `PUT /api/exercises/{id}/`

**Request**:
```bash
curl -X PUT http://localhost:8000/api/exercises/1/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"muscle\":3,\"name\":\"Bench Press\",\"note\":\"Updated: Focus on explosive movements\"}"
```

### Step 8: Create Training Sessions

**Endpoint**: `POST /api/trainings/`

**Training 1 - Bench Press**:
```bash
curl -X POST http://localhost:8000/api/trainings/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"exercise\":1,\"weight\":80.5,\"sets\":4,\"repetitions\":10}"
```

**Training 2 - Bench Press (heavier)**:
```bash
curl -X POST http://localhost:8000/api/trainings/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"exercise\":1,\"weight\":85.0,\"sets\":4,\"repetitions\":8}"
```

**Training 3 - Squats**:
```bash
curl -X POST http://localhost:8000/api/trainings/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d "{\"exercise\":2,\"weight\":100.0,\"sets\":5,\"repetitions\":12}"
```

**Expected Response** (201 Created):
```json
{
  "id": 1,
  "exercise": 1,
  "exercise_name": "Bench Press",
  "muscle_name": "chest",
  "weight": "80.50",
  "sets": 4,
  "repetitions": 10,
  "datetime": "2025-10-07T21:10:00Z"
}
```

### Step 9: View Training History

**Endpoint**: `GET /api/trainings/history/`

**All History**:
```bash
curl -X GET http://localhost:8000/api/trainings/history/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Current Week**:
```bash
curl -X GET "http://localhost:8000/api/trainings/history/?period=current_week" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Last Week**:
```bash
curl -X GET "http://localhost:8000/api/trainings/history/?period=last_week" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Last Month**:
```bash
curl -X GET "http://localhost:8000/api/trainings/history/?period=last_month" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Last Year**:
```bash
curl -X GET "http://localhost:8000/api/trainings/history/?period=last_year" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Filter by Exercise**:
```bash
curl -X GET "http://localhost:8000/api/trainings/history/?exercise=1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Filter by Muscle**:
```bash
curl -X GET "http://localhost:8000/api/trainings/history/?muscle=3" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Step 10: View Training Statistics

**Endpoint**: `GET /api/trainings/stats/`

**All Statistics**:
```bash
curl -X GET http://localhost:8000/api/trainings/stats/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response** (200 OK):
```json
[
  {
    "exercise_id": 1,
    "exercise_name": "Bench Press",
    "muscle_name": "chest",
    "low_weight": "80.50",
    "high_weight": "85.00",
    "last_weight": "85.00",
    "total_sessions": 2
  },
  {
    "exercise_id": 2,
    "exercise_name": "Squats",
    "muscle_name": "legs",
    "low_weight": "100.00",
    "high_weight": "100.00",
    "last_weight": "100.00",
    "total_sessions": 1
  }
]
```

**Filter by Exercise**:
```bash
curl -X GET "http://localhost:8000/api/trainings/stats/?exercise=1" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Filter by Muscle**:
```bash
curl -X GET "http://localhost:8000/api/trainings/stats/?muscle=3" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

### Step 11: Delete an Exercise

**Endpoint**: `DELETE /api/exercises/{id}/`

**Request**:
```bash
curl -X DELETE http://localhost:8000/api/exercises/1/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

**Expected Response**: 204 No Content

## Testing Checklist

### ✅ User Registration & Authentication
- [ ] Register new user with valid data
- [ ] Reject duplicate email
- [ ] Reject duplicate username
- [ ] Reject password < 8 characters
- [ ] Login with valid credentials
- [ ] Reject invalid credentials
- [ ] Get user profile with valid token
- [ ] Reject request without token

### ✅ Muscle Groups
- [ ] List all 9 muscle groups
- [ ] Get specific muscle by ID

### ✅ Exercises
- [ ] Create exercise for a muscle
- [ ] List all user's exercises
- [ ] Filter exercises by muscle
- [ ] Get specific exercise by ID
- [ ] Update exercise
- [ ] Delete exercise
- [ ] Verify user can only see their own exercises

### ✅ Training Sessions
- [ ] Create training session
- [ ] List all training sessions
- [ ] Get specific training by ID
- [ ] Update training session
- [ ] Delete training session
- [ ] View all training history
- [ ] Filter history by current week
- [ ] Filter history by last week
- [ ] Filter history by last month
- [ ] Filter history by last year
- [ ] Filter history by exercise
- [ ] Filter history by muscle

### ✅ Training Statistics
- [ ] Get statistics for all exercises
- [ ] Verify low_weight is minimum
- [ ] Verify high_weight is maximum
- [ ] Verify last_weight is most recent
- [ ] Filter stats by exercise
- [ ] Filter stats by muscle

### ✅ Security
- [ ] Endpoints require authentication (except register/login)
- [ ] Users can only access their own data
- [ ] JWT token expires after 24 hours
- [ ] Invalid tokens are rejected

## Common Test Scenarios

### Scenario 1: Complete User Journey
1. Register → Login → Create exercises → Log trainings → View stats
2. Verify progression over time

### Scenario 2: Multiple Users
1. Register User A and User B
2. Each creates exercises
3. Verify User A cannot see User B's exercises
4. Verify User A cannot create training for User B's exercises

### Scenario 3: Data Validation
1. Try creating training with negative weight → Should fail
2. Try creating training with 0 sets → Should fail
3. Try creating exercise without muscle → Should fail

### Scenario 4: Time-based Filtering
1. Create trainings over multiple days
2. Test each time period filter
3. Verify correct data is returned

## Using Swagger UI

1. Navigate to http://localhost:8000/api/docs/
2. Click "Authorize" button
3. Enter: `Bearer YOUR_TOKEN_HERE`
4. Click "Authorize" then "Close"
5. All endpoints are now authenticated
6. Click on any endpoint to expand
7. Click "Try it out"
8. Fill in parameters
9. Click "Execute"
10. View response

## Using Postman

1. Import `Fitness_Studio_API.postman_collection.json`
2. Run "Login" request
3. Token is automatically saved to collection variable
4. All other requests will use this token automatically
5. Test all endpoints in order

## Troubleshooting Tests

### 401 Unauthorized
- Check token is valid and not expired
- Verify Authorization header format: `Bearer <token>`

### 403 Forbidden
- User trying to access another user's data
- Check exercise/training ownership

### 400 Bad Request
- Validation error
- Check request body format
- Verify all required fields are present

### 404 Not Found
- Resource doesn't exist
- Check ID in URL
- Verify resource belongs to authenticated user

## Performance Testing

Test with multiple trainings:
```bash
# Create 100 training sessions
for i in {1..100}; do
  curl -X POST http://localhost:8000/api/trainings/ \
    -H "Authorization: Bearer YOUR_TOKEN_HERE" \
    -H "Content-Type: application/json" \
    -d "{\"exercise\":1,\"weight\":$((80 + i % 20)),\"sets\":4,\"repetitions\":10}"
done
```

Then test:
- History retrieval speed
- Stats calculation speed
- Filtering performance

## Automated Testing

Create a test script (`test_api.py`):
```python
import requests

BASE_URL = "http://localhost:8000/api"

# Register
response = requests.post(f"{BASE_URL}/auth/register/", json={
    "email": "auto@test.com",
    "password": "AutoTest123",
    "username": "autotest",
    "first_name": "Auto",
    "last_name": "Test"
})
print(f"Register: {response.status_code}")

# Login
response = requests.post(f"{BASE_URL}/auth/login/", json={
    "email": "auto@test.com",
    "password": "AutoTest123"
})
token = response.json()["token"]
headers = {"Authorization": f"Bearer {token}"}
print(f"Login: {response.status_code}")

# Create exercise
response = requests.post(f"{BASE_URL}/exercises/", 
    headers=headers,
    json={"muscle": 1, "name": "Test Exercise", "note": "Test"}
)
exercise_id = response.json()["id"]
print(f"Create Exercise: {response.status_code}")

# Create training
response = requests.post(f"{BASE_URL}/trainings/",
    headers=headers,
    json={"exercise": exercise_id, "weight": 100, "sets": 3, "repetitions": 10}
)
print(f"Create Training: {response.status_code}")

# Get stats
response = requests.get(f"{BASE_URL}/trainings/stats/", headers=headers)
print(f"Get Stats: {response.status_code}")
print(f"Stats: {response.json()}")
```

Run: `python test_api.py`
