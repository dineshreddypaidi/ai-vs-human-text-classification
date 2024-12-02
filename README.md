# AI vs Human Text Classification API

This project provides an API for user authentication, text classification (AI-generated vs. human-generated), and retrieval of classification history.

## Table of Contents

- [Base URL](#base-url)
- [Authentication](#authentication)
- [Endpoints](#endpoints)
  - [Index](#1-index)
  - [Register](#2-register)
  - [Login](#3-login)
  - [Logout](#4-logout)
  - [Get User Profile](#5-get-user-profile)
  - [Predict](#6-predict)
  - [History](#7-history)
- [Response Codes](#response-codes)
- [License](#license)

---

## Base URL

```
http://your-domain.com/ or http://localhost
```

---

## Authentication

Most endpoints require user authentication. Use **session authentication** for requests. Ensure the user is logged in where required.

---

## Endpoints

### 1. Index

- **URL**: `/`
- **Method**: `GET`
- **Description**: Basic endpoint to verify if the API is running.

#### Response (Success - 200)

```json
{
  "result": "hello"
}
```

---

### 2. Register

- **URL**: `/register/`
- **Method**: `POST`
- **Description**: Registers a new user.

#### Request Body (JSON or `application/x-www-form-urlencoded`)

```json
{
  "username": "your_username",
  "password": "your_password",
  "email": "your_email@example.com",
  "name": "your_name"
}
```

#### Response (Success - 200)

```json
{
  "message": "User registered in successfully"
}
```

#### Response (Error - 405)

```json
{
  "error": "Username already exists"
}
```

---

### 3. Login

- **URL**: `/login/`
- **Method**: `POST`
- **Description**: Authenticates a user and starts a session.

#### Request Body (JSON or `application/x-www-form-urlencoded`)

```json
{
  "username": "your_username",
  "password": "your_password"
}
```

#### Response (Success - 200)

```json
{
  "message": "User logged in successfully"
}
```

#### Response (Error - 404)

```json
{
  "error": "Invalid username or password"
}
```

---

### 4. Logout

- **URL**: `/logout/`
- **Method**: `POST`
- **Description**: Logs out the authenticated user.

#### Response (Success - 200)

```json
{
  "message": "logout successful"
}
```

---

### 5. Get User Profile

- **URL**: `/user/`
- **Method**: `GET`
- **Description**: Retrieves the authenticated user's profile information.

#### Response (Success - 200)

```json
{
  "data": {
    "username": "your_username",
    "email": "your_email@example.com",
    "name": "your_name",
    "last login": "2024-11-01T12:34:56Z",
    "phone number": null,
    "enquires": 0
  }
}
```

#### Response (Error - 401)

```json
{
  "message": "is not authenticated"
}
```

---

### 6. Predict

- **URL**: `/predict/`
- **Method**: `POST`
- **Description**: Predicts if the provided text is AI-generated or human-generated.

#### Request Body

```json
{
  "text": "Your text to classify here."
}
```

#### Response (Success - 200)

```json
{
  "prediction": "Ai generated or human generated",
  "accuracy": "accuracy of the prediction"
}
```

#### Response (Error - 401)

```json
{
  "message": "is not authenticated"
}
```

---

### 7. History

- **URL**: `/history/`
- **Method**: `GET`
- **Description**: Retrieves the history of classification results for the authenticated user.

#### Response (Success - 200)

```json
{
  "history": [
    {
      "user": "your_username",
      "text": "Sample text here",
      "result": "AI"
    },
    {
      "user": "your_username",
      "text": "Another sample text",
      "result": "Human"
    }
  ]
}
```

#### Response (Error - 401)

```json
{
  "message": "is not authenticated"
}
```

---

## Response Codes

| Code | Meaning                |
| ---- | ---------------------- |
| 200  | Success                |
| 400  | Bad Request            |
| 401  | Unauthorized           |
| 404  | Not Found              |
| 405  | Method Not Allowed     |
| 415  | Unsupported Media Type |

---

## License

This project is licensed under the MIT License.

---
