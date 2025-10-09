# Login Guide - Email or Username

The Fitness Studio API supports **flexible login** - you can use either your **email** or **username (nickname)** to authenticate.

## Quick Reference

### Field Name
Use `email_or_username` in your login requests (not just `email`)

### Accepted Values
- ✅ Email address: `user@example.com`
- ✅ Username (nickname): `johndoe`

---

## Examples

### 1. Login with Email

**Request:**
```json
POST /api/auth/login/
Content-Type: application/json

{
  "email_or_username": "john@example.com",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2025-10-07T21:00:00Z"
  },
  "message": "Login successful"
}
```

### 2. Login with Username

**Request:**
```json
POST /api/auth/login/
Content-Type: application/json

{
  "email_or_username": "johndoe",
  "password": "SecurePass123"
}
```

**Response:**
```json
{
  "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "date_joined": "2025-10-07T21:00:00Z"
  },
  "message": "Login successful"
}
```

---

## How It Works

The API automatically detects whether you're using an email or username:

- **Contains `@`** → Treated as email
- **No `@`** → Treated as username

---

## Using Different Tools

### curl (Windows CMD)

**With email:**
```cmd
curl -X POST http://localhost:8000/api/auth/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email_or_username\":\"john@example.com\",\"password\":\"SecurePass123\"}"
```

**With username:**
```cmd
curl -X POST http://localhost:8000/api/auth/login/ ^
  -H "Content-Type: application/json" ^
  -d "{\"email_or_username\":\"johndoe\",\"password\":\"SecurePass123\"}"
```

### PowerShell

```powershell
# With email
$body = @{
    email_or_username = "john@example.com"
    password = "SecurePass123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method Post -Body $body -ContentType "application/json"

# With username
$body = @{
    email_or_username = "johndoe"
    password = "SecurePass123"
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/api/auth/login/" -Method Post -Body $body -ContentType "application/json"
```

### Python

```python
import requests

# With email
response = requests.post(
    "http://localhost:8000/api/auth/login/",
    json={
        "email_or_username": "john@example.com",
        "password": "SecurePass123"
    }
)

# With username
response = requests.post(
    "http://localhost:8000/api/auth/login/",
    json={
        "email_or_username": "johndoe",
        "password": "SecurePass123"
    }
)

token = response.json()["token"]
```

### JavaScript (Fetch API)

```javascript
// With email
fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email_or_username: 'john@example.com',
    password: 'SecurePass123'
  })
})
.then(response => response.json())
.then(data => console.log(data.token));

// With username
fetch('http://localhost:8000/api/auth/login/', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email_or_username: 'johndoe',
    password: 'SecurePass123'
  })
})
.then(response => response.json())
.then(data => console.log(data.token));
```

### Swagger UI

1. Go to http://localhost:8000/api/docs/
2. Expand `POST /api/auth/login/`
3. Click "Try it out"
4. In the request body, enter:
   ```json
   {
     "email_or_username": "john@example.com",
     "password": "SecurePass123"
   }
   ```
   OR
   ```json
   {
     "email_or_username": "johndoe",
     "password": "SecurePass123"
   }
   ```
5. Click "Execute"
6. Copy the token from the response

### Postman

Import the `Fitness_Studio_API.postman_collection.json` file. It includes two login requests:
- **Login (with email)** - Pre-configured with email example
- **Login (with username)** - Pre-configured with username example

Both automatically save the token to collection variables.

---

## Error Handling

### Invalid Credentials

**Request:**
```json
{
  "email_or_username": "john@example.com",
  "password": "WrongPassword"
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Invalid credentials. Please check your email/username and password."
}
```

### Missing Fields

**Request:**
```json
{
  "email_or_username": "john@example.com"
}
```

**Response (400 Bad Request):**
```json
{
  "password": ["This field is required."]
}
```

---

## Using the Token

After successful login, use the token in the `Authorization` header:

```
Authorization: Bearer YOUR_TOKEN_HERE
```

**Example:**
```bash
curl -X GET http://localhost:8000/api/auth/profile/ ^
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc..."
```

---

## Token Expiration

- Tokens are valid for **24 hours**
- After expiration, login again to get a new token
- No refresh token mechanism (yet)

---

## Security Notes

- Always use HTTPS in production
- Never share your token
- Store tokens securely (not in localStorage for sensitive apps)
- Tokens contain user ID and email (but are signed and cannot be tampered with)

---

## Backward Compatibility

⚠️ **Breaking Change from v1.0.0**

If you were using the old login format:
```json
{
  "email": "user@example.com",
  "password": "password"
}
```

You must update to:
```json
{
  "email_or_username": "user@example.com",
  "password": "password"
}
```

See `CHANGELOG.md` for migration details.

---

## Need Help?

- Check the interactive docs: http://localhost:8000/api/docs/
- See `API_TESTING_GUIDE.md` for more examples
- See `README.md` for complete documentation
