# Auth_forge API Reference

Comprehensive specification of all endpoints available in the **Auth_forge** authentication service.

- **Base URL**: `http://localhost:8000`
- **Interactive OpenAPI Documentation**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## Overview & Authentication Flow

Auth_forge implements stateless JSON Web Token (JWT) authentication:
1. **Register** a new user account with `POST /users`.
2. **Authenticate** using `POST /auth/login` to obtain a signed JWT `access_token`.
3. **Access protected routes** (like `GET /users/me`) by providing the token in the `Authorization` header:
   ```http
   Authorization: Bearer <your_access_token>
   ```

---

## Summary of Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API health check / welcome banner | No |
| `POST` | `/users` | Register a new user | No |
| `POST` | `/auth/login` | Authenticate credentials and issue JWT token | No |
| `GET` | `/users/me` | Retrieve the authenticated user's profile | **Yes (Bearer JWT)** |
| `GET` | `/users/{user_id}` | Retrieve public user info by ID | No |

---

## Detailed Endpoint Documentation

### 1. Root / Health Check

Checks if the service is running.

- **Endpoint**: `GET /`
- **Authentication**: None

#### Response (`200 OK`)
```json
{
  "message": "Authentication API is running"
}
```

#### Example Request
```bash
curl -X GET http://localhost:8000/
```

---

### 2. User Registration

Creates a new user record with hashed password (Argon2) and default active status.

- **Endpoint**: `POST /users`
- **Authentication**: None
- **Status Code**: `201 Created`

#### Request Body (`application/json`)
| Field | Type | Constraints | Description |
| :--- | :--- | :--- | :--- |
| `email` | string (email) | Valid email format | User's unique email address |
| `username` | string | 3–100 characters | Unique username |
| `password` | string | Minimum 8 characters | Plaintext password to hash |

```json
{
  "email": "user@example.com",
  "username": "alexdev",
  "password": "StrongPassword123!"
}
```

#### Response (`201 Created`)
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "alexdev",
  "is_active": true,
  "is_verified": false
}
```

#### Error Responses
- **`409 Conflict`**: Email or username already exists.
  ```json
  {
    "detail": "Email or username already exists"
  }
  ```
- **`422 Unprocessable Entity`**: Validation failure (e.g. invalid email format, short password).

#### Example Request
```bash
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "alexdev",
    "password": "StrongPassword123!"
  }'
```

---

### 3. User Login

Validates username and password against stored Argon2 hash, confirms active status, and returns a signed JWT.

- **Endpoint**: `POST /auth/login`
- **Authentication**: None
- **Status Code**: `200 OK`

#### Request Body (`application/json`)
| Field | Type | Description |
| :--- | :--- | :--- |
| `username` | string | Registered account username |
| `password` | string | Plaintext account password |

```json
{
  "username": "alexdev",
  "password": "StrongPassword123!"
}
```

#### Response (`200 OK`)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

#### Error Responses
- **`401 Unauthorized`**: Non-existent username or invalid password.
  ```json
  {
    "detail": "Invalid username or password"
  }
  ```
- **`403 Forbidden`**: Account deactivated (`is_active = false`).
  ```json
  {
    "detail": "Account is inactive"
  }
  ```

#### Example Request
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alexdev",
    "password": "StrongPassword123!"
  }'
```

---

### 4. Get Current Authenticated User (`/users/me`)

Protected endpoint that extracts the Bearer token, validates its signature and expiration, retrieves the user, and returns their profile.

- **Endpoint**: `GET /users/me`
- **Authentication**: **Bearer Token (JWT)**
- **Status Code**: `200 OK`

#### Request Headers
```http
Authorization: Bearer <your_jwt_access_token>
```

#### Response (`200 OK`)
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "alexdev",
  "is_active": true,
  "is_verified": false
}
```

#### Error Responses
- **`401 Unauthorized`**: Missing, expired, or invalid token.
  ```json
  {
    "detail": "Invalid or expired token"
  }
  ```
- **`403 Forbidden`**: Account inactive.
  ```json
  {
    "detail": "Account is inactive"
  }
  ```

#### Example Request
```bash
curl -X GET http://localhost:8000/users/me \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
```

---

### 5. Get User by ID

Fetches a user profile by their numeric database ID.

- **Endpoint**: `GET /users/{user_id}`
- **Authentication**: None
- **Status Code**: `200 OK`

#### Path Parameters
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `user_id` | integer | Numeric primary key ID of user |

#### Response (`200 OK`)
```json
{
  "id": 1,
  "email": "user@example.com",
  "username": "alexdev",
  "is_active": true,
  "is_verified": false
}
```

#### Error Responses
- **`404 Not Found`**:
  ```json
  {
    "detail": "User not found"
  }
  ```

#### Example Request
```bash
curl -X GET http://localhost:8000/users/1
```
