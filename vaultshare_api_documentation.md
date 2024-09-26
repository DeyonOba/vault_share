# VaultShare API Documentation

## Overview
VaultShare is a file-sharing and workspace management API that allows users to create
accounts, manage workspaces and interact with files and directories.
This documentation outlines the available API routes, their purposes, and the expected
request and response formats.

## Running the Application
To start the VaultShare application, run the following command:
```bash
chmod +x main.py
./main.py
```
OR
```bash
python3 main.py
```
This will start the app on `http://0.0.0.0:5000`

## Base URL

```bash
http://localhost:5000
```
***
## - `GET /`

#### Description:
The root endpoint of VaultShare. Displays a welcome message to unauthenticated
users or redirect logged-in users to their account information.

#### Request:
- **Method**: GET
- **URL**: /

#### Curl Example:
```bash
curl -X GET http://localhost:5000/
```
#### Response:
```json
{
    "message": "Welcome to VaultShare"
}
```
#### Status Codes:
- **200 OK**
***
## - `GET /status`
#### Description:
The health check endpoint returns the status of the VaultShare API.

#### Request:
- **Method**: `GET`
- **URL**: `/status`
#### Curl Example:
```bash
curl -X GET http://localhost:5000/status
```
#### Response:
```json
{
    "status": "OK"
}
```
#### Status Codes:
- **200 OK**
***
## - `POST /signup`
#### Description:
Handles user account creation. Creates a new user in the system.

#### Request:
- **Method**: POST
- **URL**: /signup
#### Form Data:
- **username**: (string) Required.
- **email**: (string) Required.
- **password**: (string) Required.
#### Curl Example:
```bash
curl -X POST http://localhost:5000/signup \
     -F "username=johndoe" \
     -F "email=johndoe@example.com" \
     -F "password=mysecurepassword"
```
#### Response:
```json
{
    "message": "Awesome! johndoe you are now a member of VaultShare family",
    "account_detail": {
        "username": "johndoe",
        "email": "johndoe@example.com",
        "role": "user",
        "created_at": "2024-09-25T12:34:56"
    },
    "recommended_actions": ["login", "create_workspace", "join_workspace"]
}
```
#### Status Codes:
- **201 Created**
- **422 Unprocessable Entity** – Invalid field types.
- **402 Missing Field** – Missing required fields.
- **400 Bad Request** – Other errors.
- **409 Conflict** – User already exists.

## - `POST /login`
#### Description:
Logs in a user to the VaultShare system by validating either their username or email,
and password.

#### Request:
- **Method**: `POST`
- **URL**: `/login`
- **Form Data:**
    - `username` (string): Optional if `email` is provided.
    - `email` (string): Optional if the `username` is provided.
    - `password` (string): Required.
#### Curl Example:
```bash
curl -X POST http://localhost:5000/login \
     -F "email=johndoe@example.com" \
     -F "password=mysecurepassword"
```
#### Response
```json
{
    "message": "Welcome back johndoe to VaultShare",
    "session_id": "123456789abcdef",
    "recommend_actions": ["checkNotification", "createWorkspace", "joinWorkspace"]
}
```
#### Status Codes:
- **200 OK**
- **403 Forbidden** - Unauthorized access.
- **400 Bad Request** - Invalid login information.
***
## - DELETE /logout
#### Description:
Logs out a user by destroying their session.

#### Request:
- **Method**: `DELETE`
- **URL**: `/logout`
- **Cookies**: `session_id` (string) Required.

#### Curl Example:
```bash
{
    "message": "Welcome back johndoe to VaultShare",
    "session_id": "123456789abcdef",
    "recommend_actions": ["checkNotification", "createWorkspace", "joinWorkspace"]
}
```
#### Response:
Redirects to `/`.

#### Status Codes:
- **403 Forbidden** – Unauthorized access (missing or invalid session).
- **422 Unprocessable Entity** – Failed to destroy the session.
***
## Error Handling
#### - 403 Forbidden
This error is returned when the user is not authorized to access the requested resource.

```json
{
    "error": "Unauthorized access"
}
```
#### - 402 Missing Field
This error occurs when required fields are missing in the request.
```json
{
    "error": "Fill in your <field>"
}
```

#### - 422 Unprocessable Entity
This error occurs when invalid field types are provided in the request.

```json
{
    "error": "Invalid <field> type"
}
```
#### -  400 Bad Request
This error occurs when there is a general error in the request, such as invalid input.

```json
{
    "error": "Bad request error"
}
```
