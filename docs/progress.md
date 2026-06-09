# AI E-Commerce Analytics Platform - Progress Log

---

# Day 1 - FastAPI Foundation

## Objective

Set up the backend foundation and CI/CD pipeline.

## Tasks Completed

### Project Setup

* Created GitHub repository
* Cloned repository locally
* Created backend directory
* Created Python virtual environment
* Installed project dependencies

### FastAPI Setup

Created:

```text
backend/app/main.py
```

Implemented:

* Root endpoint (`/`)
* Health endpoint (`/health`)
* Swagger UI (`/docs`)
* OpenAPI documentation

### Configuration Management

Created:

```text
backend/app/core/config.py
```

Implemented:

* Pydantic Settings
* Environment Variable Support
* Application Configuration Management

### CI/CD

Created:

```text
.github/workflows/backend-ci.yml
```

Pipeline includes:

* Repository checkout
* Python setup
* Dependency installation
* FastAPI application validation

### Issues Faced

Problem:

```text
GitHub Actions failed because environment variables were mandatory.
```

Resolution:

```text
Added default values in Pydantic Settings.
```

### Skills Learned

* FastAPI Fundamentals
* Environment Variables
* GitHub Actions
* CI/CD Basics
* Configuration Management

### Status

✅ Completed

---

# Day 2 - Docker Infrastructure

## Objective

Containerize the application and create local development infrastructure.

## Tasks Completed

### Docker Setup

Verified:

```bash
docker --version
docker run hello-world
```

### Dockerfile

Created:

```text
backend/Dockerfile
```

Concepts Learned:

* Docker Image
* Docker Container
* Build Process
* Container Lifecycle

### PostgreSQL Container

Implemented:

```yaml
postgres:
```

Features:

* PostgreSQL 17
* Persistent Storage
* Volume Management

Concept Learned:

```text
Containers are temporary.
Volumes persist data.
```

### Redis Container

Implemented:

```yaml
redis:
```

Features:

* Redis 8
* In-memory caching layer

### Docker Compose

Created:

```text
docker-compose.yml
```

Implemented:

* PostgreSQL Service
* Redis Service
* Backend Service

### Networking Concepts Learned

#### localhost

Inside a container:

```text
localhost = current container
```

#### Service Discovery

Backend connects using:

```text
postgres
redis
```

instead of:

```text
localhost
```

#### Docker DNS

Docker automatically resolves:

```text
postgres -> container IP
redis -> container IP
```

### Environment Variables

Created:

```text
backend/.env
```

Added:

* APP_NAME
* APP_VERSION
* ENVIRONMENT
* DATABASE_URL
* REDIS_URL

### FastAPI Integration

Backend now runs through:

```bash
docker compose up -d
```

Architecture:

```text
backend
   |
   +---- postgres
   |
   +---- redis
```

### Issues Faced

#### Issue 1

Problem:

```text
Backend container did not start.
```

Cause:

```text
Old manually created container was already using port 8000.
```

Resolution:

```bash
docker stop vigilant_ellis
docker rm vigilant_ellis
docker compose up --build -d
```

### Skills Learned

* Docker
* Docker Compose
* Docker Networking
* Volumes
* Service Discovery
* Multi-container Applications

### Status

✅ Completed

---

# Day 3 - Planned

## Objective

Build database foundation using SQLAlchemy.

## Planned Tasks

* Create db module
* SQLAlchemy setup
* Database session management
* Base model
* User model
* User schema
* Industry standard project structure

Status: 🚧 Pending


# Day-3

Day 3 Learning

- Difference between Model and Schema
- Database Normalization
- One-to-Many Relationships
- SQLAlchemy Engine
- SQLAlchemy Session
- Why Orders and Addresses belong in separate tables


# Day-4

Day 4

Completed:
- Created User SQLAlchemy Model
- Created Users PostgreSQL Table
- Implemented Pydantic Request/Response Schemas
- Implemented Repository Pattern
- Implemented Database Session Dependency
- Added APIRouter for Users
- Built POST /users endpoint
- Inserted first user into PostgreSQL
- Verified data directly from PostgreSQL

Key Learnings:
- Model vs Schema
- Engine vs Session
- Database Normalization
- Repository Pattern
- Docker Networking
- Service Layer Architecture
- Full Request Lifecycle:
  Swagger → Route → Schema → Repository → Session → Engine → PostgreSQL


# 5 Day 5

Completed:
- Added Service Layer Architecture
- Implemented Email Uniqueness Validation
- Added Password Hashing with bcrypt
- Created Security Module
- Fixed bcrypt/passlib dependency issue
- Successfully stored hashed passwords in PostgreSQL

Key Learnings:
- Business Logic belongs in Services
- Repository Pattern
- Password Hashing vs Encryption
- bcrypt Salted Hashing
- Dependency Version Conflicts
- Debugging FastAPI using Docker Logs