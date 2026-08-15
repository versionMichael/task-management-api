# Task Management API

A RESTful task management backend built with **FastAPI**, **PostgreSQL**, **SQLAlchemy**, and **JWT authentication**.

The API allows authenticated users to create and manage projects and tasks while enforcing ownership and authorization rules.

**Live API:** https://task-management-api-production-47aa.up.railway.app

**Swagger Docs:** https://task-management-api-production-47aa.up.railway.app/docs

---

## 🚀 Features

- User registration and authentication
- JWT-based authentication
- Password hashing
- User management
- Project CRUD operations
- Task CRUD operations
- Assign tasks to users
- Move tasks between projects
- Project and task ownership authorization
- Pydantic request and response validation
- PostgreSQL database
- SQLAlchemy ORM
- Automated API testing with pytest
- Separate PostgreSQL test database
- Environment variable configuration
- Dockerized FastAPI application
- Docker Compose for FastAPI and PostgreSQL
- Persistent PostgreSQL storage with Docker volumes
- PostgreSQL health checks

---

## 🛠️ Tech Stack

- **Python**
- **FastAPI**
- **PostgreSQL**
- **SQLAlchemy**
- **Pydantic**
- **JWT**
- **pwdlib**
- **pytest**
- **python-dotenv**
- **Uvicorn**
- **Docker**
- **Docker Compose**

---

## 📸 Screenshots

### API Documentation
![Swagger API Documentation](screenshots/swagger.png)

### Automated Tests
![33 Tests Passed](screenshots/tests.png)

### Dockerized Deployment
![Docker FastAPI and PostgreSQL](screenshots/docker.png)

---

## 📁 Project Structure

```text
task-management-api/
├── app/
├── tests/
├── screenshots/
├── .dockerignore
├── .env.example
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
└── README.md
```

---

## 🔐 Authentication

The API uses **JWT Bearer tokens** for authentication.

Users first register an account and then log in to receive an access token.

Protected endpoints require:

```text
Authorization: Bearer <access_token>
```

Users can only access, modify, or delete projects and tasks that belong to projects they own.

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/auth/login` | Log in and receive a JWT |

### Users

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/users/` | Create a user |
| `GET` | `/users/` | Get users |
| `GET` | `/users/{user_id}` | Get a specific user |
| `PUT` | `/users/{user_id}` | Update a user |
| `DELETE` | `/users/{user_id}` | Delete a user |
| `GET` | `/users/{user_id}/projects` | Get a user's projects |
| `GET` | `/users/{user_id}/tasks` | Get a user's assigned tasks |

### Projects

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/projects/` | Get projects |
| `GET` | `/projects/{project_id}` | Get a specific project |
| `POST` | `/projects/` | Create a project |
| `PUT` | `/projects/{project_id}` | Update a project |
| `DELETE` | `/projects/{project_id}` | Delete a project |
| `GET` | `/projects/{project_id}/tasks` | Get tasks belonging to a project |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/tasks/` | Get tasks from the user's projects |
| `GET` | `/tasks/{task_id}` | Get a specific task |
| `POST` | `/tasks/` | Create a task |
| `PUT` | `/tasks/{task_id}` | Update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |
| `GET` | `/tasks/{task_id}/user` | Get the user assigned to a task |

A task can also be moved between projects by updating its `project_id`, provided the user owns both projects.

---

## 🗄️ Database

The application uses **PostgreSQL** with **SQLAlchemy** as the ORM.

```text
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

Tasks contain `project_id` and `assigned_to`.

---

## ⚙️ Environment Variables

For local development, create a `.env` file:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/task_management
```

For testing, create `.env.test`:

```env
TEST_DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/task_management_test
```

For Docker, create `.env.docker`:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=YOUR_DOCKER_PASSWORD
POSTGRES_DB=task_management
```

These files contain local credentials and should not be committed to GitHub. An `.env.example` file is included for reference.

---

## 📦 Installation

```bash
git clone https://github.com/versionMichael/task-management-api
cd task-management-api
python -m venv .venv
```

Activate on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🗃️ Database Setup

For local development, create the PostgreSQL databases specified in `.env` and `.env.test`.

When using Docker Compose, PostgreSQL is created and managed automatically by the PostgreSQL container.

---

## 🐳 Running with Docker

Make sure Docker Desktop is running, then:

```bash
docker compose --env-file .env.docker up --build
```

Docker Compose will build the FastAPI image, start PostgreSQL 17, create persistent storage, run a health check, wait for PostgreSQL to become healthy, and start Uvicorn.

The API will be available at:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

Stop the containers with `Ctrl+C`.

---

## ▶️ Running the API Locally

Without Docker:

```bash
uvicorn app.main:app --reload
```

API:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

You can use Swagger to register users, log in, authorize with a JWT, and test protected endpoints.

---

## 🧪 Running Tests

Run the complete test suite:

```bash
pytest
```

The tests use a separate PostgreSQL test database so application data is not affected.

The suite contains **33 tests** covering:

- Authentication
- JWT authentication failures
- User operations and authorization
- Project operations and ownership
- Task operations and ownership
- Task assignment
- Moving tasks between projects

**All 33 tests pass.**

---

## 🔬 Testing Strategy

Reusable pytest fixtures are defined in `tests/conftest.py`.

The `client` fixture provides a FastAPI `TestClient` connected to the test database.

The `test_user` fixture creates unique test users using UUIDs so tests do not conflict with one another.

---

## 🛡️ Authorization

The API enforces ownership at the project level.

```text
User A
  │
  └── Project A
        │
        └── Task A
```

User A can access and modify Project A and Task A.

Another user cannot access, modify, or delete User A's project or its tasks.

Unauthenticated requests return `401 Unauthorized`.

Authenticated users attempting to access resources they do not own receive `403 Forbidden`.

---

## ❌ Error Handling

| Status Code | Meaning |
|---|---|
| `200` | Successful request |
| `401` | Authentication required or invalid credentials/token |
| `403` | Authenticated but not authorized |
| `404` | Requested resource does not exist |

---

## 🔒 Security

- Passwords are hashed before being stored.
- Passwords and password hashes are not returned in API responses.
- Protected endpoints require JWT authentication.
- Users cannot access or modify projects they do not own.
- Users cannot access or modify tasks belonging to another user's project.
- Environment files containing credentials are excluded from version control.
