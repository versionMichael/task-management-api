# Task Management API

A RESTful task management backend built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **JWT authentication**.

The API allows authenticated users to create and manage projects and
tasks while enforcing ownership and authorization rules.

**Live API:** https://task-management-api-production-47aa.up.railway.app

**Swagger Docs:** https://task-management-api-production-47aa.up.railway.app/docs

---

------------------------------------------------------------------------

## 🚀 Features

-   User registration and authentication
-   JWT-based authentication
-   Password hashing
-   User management
-   Project CRUD operations
-   Task CRUD operations
-   Assign tasks to users
-   Move tasks between projects
-   Project and task ownership authorization
-   Pydantic request and response validation
-   PostgreSQL database
-   SQLAlchemy ORM
-   Automated API testing with pytest
-   Separate PostgreSQL test database
-   Environment variable configuration
-   Dockerized FastAPI application
-   Docker Compose for FastAPI and PostgreSQL
-   Persistent PostgreSQL storage with Docker volumes
-   PostgreSQL health checks

------------------------------------------------------------------------

## 🛠️ Tech Stack

-   **Python**
-   **FastAPI**
-   **PostgreSQL**
-   **SQLAlchemy**
-   **Pydantic**
-   **JWT**
-   **pwdlib**
-   **pytest**
-   **python-dotenv**
-   **Uvicorn**
-   **Docker**
-   **Docker Compose**

------------------------------------------------------------------------

## 📁 Project Structure

``` text
task-management-api/
│
├── app/
│   ├── core/
│   ├── models/
│   │   ├── project.py
│   │   ├── task.py
│   │   └── user.py
│   ├── routers/
│   │   ├── auth.py
│   │   ├── project.py
│   │   ├── task.py
│   │   └── user.py
│   ├── schemas/
│   │   ├── project.py
│   │   ├── task.py
│   │   └── user.py
│   ├── services/
│   ├── utils/
│   │   └── auth.py
│   ├── database.py
│   └── main.py
│
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_projects.py
│   └── test_tasks.py
│
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

------------------------------------------------------------------------

## 🔐 Authentication

The API uses **JWT Bearer tokens** for authentication.

Users first register an account and then log in to receive an access
token.

Protected endpoints require the token in the request header:

``` text
Authorization: Bearer <access_token>
```

Users can only access, modify, or delete projects and tasks that belong
to projects they own.

------------------------------------------------------------------------

## 📡 API Endpoints

### Authentication

   Method  Endpoint        Description
  -------- --------------- --------------------------
   `POST`  `/auth/login`   Log in and receive a JWT

### Users

    Method   Endpoint                      Description
  ---------- ----------------------------- -----------------------------
    `POST`   `/users/`                     Create a user
    `GET`    `/users/`                     Get users
    `GET`    `/users/{user_id}`            Get a specific user
    `PUT`    `/users/{user_id}`            Update a user
   `DELETE`  `/users/{user_id}`            Delete a user
    `GET`    `/users/{user_id}/projects`   Get a user's projects
    `GET`    `/users/{user_id}/tasks`      Get a user's assigned tasks

### Projects

  -------------------------------------------------------------------------------------
               Method              Endpoint                         Description
  -------------------------------- -------------------------------- -------------------
               `GET`               `/projects/`                     Get projects

               `GET`               `/projects/{project_id}`         Get a specific
                                                                    project

               `POST`              `/projects/`                     Create a project

               `PUT`               `/projects/{project_id}`         Update a project

              `DELETE`             `/projects/{project_id}`         Delete a project

               `GET`               `/projects/{project_id}/tasks`   Get tasks belonging
                                                                    to a project
  -------------------------------------------------------------------------------------

### Tasks

    Method   Endpoint                  Description
  ---------- ------------------------- ------------------------------------
    `GET`    `/tasks/`                 Get tasks from the user's projects
    `GET`    `/tasks/{task_id}`        Get a specific task
    `POST`   `/tasks/`                 Create a task
    `PUT`    `/tasks/{task_id}`        Update a task
   `DELETE`  `/tasks/{task_id}`        Delete a task
    `GET`    `/tasks/{task_id}/user`   Get the user assigned to a task

A task can also be moved between projects by updating its `project_id`
through the task update endpoint, provided the user owns both projects.

------------------------------------------------------------------------

## 🗄️ Database

The application uses **PostgreSQL** with **SQLAlchemy** as the ORM.

The main relationships are:

``` text
User
 │
 ├── owns Projects
 │       │
 │       └── contains Tasks
 │                  │
 │                  └── assigned to User
 │
 └── can be assigned Tasks
```

Projects contain an `owner_id`, which is used to enforce authorization.

Tasks contain:

-   `project_id`
-   `assigned_to`

This allows tasks to belong to projects and be assigned to users.

------------------------------------------------------------------------

## ⚙️ Environment Variables

For local development, create a `.env` file in the project root.

Example:

``` env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/task_management
```

For testing, create a separate `.env.test` file:

``` env
TEST_DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/task_management_test
```

For Docker, create a `.env.docker` file:

``` env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=YOUR_DOCKER_PASSWORD
POSTGRES_DB=task_management
```

The `.env`, `.env.test`, and `.env.docker` files contain local
credentials and should not be committed to GitHub.

An `.env.example` file is included so the required local environment
variables can be seen without exposing credentials.

------------------------------------------------------------------------

## 📦 Installation

Clone the repository and enter the project directory:

``` bash
git clone https://github.com/versionMichael/task-management-api
cd task-management-api
```

Create a virtual environment:

``` bash
python -m venv .venv
```

Activate it on Windows:

``` powershell
.venv\Scripts\Activate.ps1
```

Install the dependencies:

``` bash
pip install -r requirements.txt
```

------------------------------------------------------------------------

## 🗃️ Database Setup

For local development, create the PostgreSQL databases used by the
application and tests.

The application database should match the database specified in `.env`.

The test database should match the database specified in `.env.test`.

When using Docker Compose, PostgreSQL is created and managed
automatically by the PostgreSQL container.

------------------------------------------------------------------------

## 🐳 Running with Docker

The project uses **Docker Compose** to run the FastAPI application and
PostgreSQL database as separate containers.

Make sure Docker Desktop is running, then start the application with:

``` bash
docker compose --env-file .env.docker up --build
```

Docker Compose will:

1.  Build the FastAPI application image from the `Dockerfile`.
2.  Pull and start the PostgreSQL 17 image.
3.  Create a persistent PostgreSQL volume.
4.  Run a PostgreSQL health check.
5.  Wait for PostgreSQL to become healthy before starting the API.
6.  Start the FastAPI application with Uvicorn.

The API will be available at:

``` text
http://localhost:8000
```

### Interactive API Documentation

Open the Swagger documentation at:

``` text
http://localhost:8000/docs
```

To stop the containers, press `Ctrl+C` in the terminal running Docker
Compose.

------------------------------------------------------------------------

## ▶️ Running the API Locally

If you are not using Docker, start the development server with:

``` bash
uvicorn app.main:app --reload
```

The API will be available at:

``` text
http://localhost:8000
```

FastAPI provides interactive Swagger documentation at:

``` text
http://localhost:8000/docs
```

You can use the `/docs` interface to register users, log in, authorize
with a JWT, and test the protected endpoints.

------------------------------------------------------------------------

## 🧪 Running Tests

The project uses **pytest** for automated testing.

Run the complete test suite with:

``` bash
pytest
```

The tests use a separate PostgreSQL test database so application data is
not affected.

### Test Coverage

The test suite contains **33 tests** covering:

-   Authentication
-   JWT authentication failures
-   User operations
-   User authorization
-   Project operations
-   Project ownership
-   Task operations
-   Task ownership
-   Task assignment
-   Moving tasks between projects

**All 33 tests pass.**

------------------------------------------------------------------------

## 🔬 Testing Strategy

The tests use reusable pytest fixtures defined in `tests/conftest.py`.

The `client` fixture provides a FastAPI `TestClient` connected to the
test database.

The `test_user` fixture automatically creates a unique test user using
UUIDs so tests do not conflict with one another.

Example:

``` python
def test_create_project(client, test_user):
    ...
```

This allows tests to reuse the same setup without manually creating
users for every test.

------------------------------------------------------------------------

## 🛡️ Authorization

The API enforces ownership at the project level.

For example:

``` text
User A
  │
  └── Project A
        │
        └── Task A
```

User A can access and modify Project A and Task A.

Another user:

``` text
User B
```

cannot access, modify, or delete User A's project or its tasks.

### Response Codes

Unauthenticated requests return:

``` text
401 Unauthorized
```

Authenticated users attempting to access resources they do not own
receive:

``` text
403 Forbidden
```

------------------------------------------------------------------------

## ❌ Error Handling

The API returns appropriate HTTP status codes for common errors:

   Status Code  Meaning
  ------------- ------------------------------------------------------
      `200`     Successful request
      `401`     Authentication required or invalid credentials/token
      `403`     Authenticated but not authorized
      `404`     Requested resource does not exist

------------------------------------------------------------------------

## 🔒 Security

-   Passwords are hashed before being stored.
-   Passwords and password hashes are not returned in API responses.
-   Protected endpoints require JWT authentication.
-   Users cannot access or modify projects they do not own.
-   Users cannot access or modify tasks belonging to another user's
    project.
-   Environment files containing credentials are excluded from version
    control.
