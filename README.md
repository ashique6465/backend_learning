# Backend Learning Repository

A comprehensive learning repository covering essential backend development concepts with practical FastAPI implementations. This repository is organized into modular sections, each focusing on specific backend patterns and technologies.

## 📚 Table of Contents

- [Quick Start](#quick-start)
- [Repository Structure](#repository-structure)
- [Module Descriptions](#module-descriptions)
- [Learning Path](#learning-path)
- [Common Setup](#common-setup)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Docker & Docker Compose (for services like PostgreSQL, Redis, Kafka)
- pip package manager

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd backend_learning
```

2. Each module has its own `requirements.txt`. Navigate to the module and install dependencies:
```bash
cd <module-name>
pip install -r requirements.txt
```

3. Run individual modules:
```bash
# For simple modules
python main.py

# For modules with Docker services
docker-compose up
# In another terminal:
python <script-name>.py
```

---

## 📁 Repository Structure

```
backend_learning/
├── api_versioning/          # API version management patterns
├── auth_api/                # Authentication & JWT implementation
├── crud_api/                # Complete CRUD operations with auth
├── dependency_injection/    # FastAPI dependency injection patterns
├── Error_handling/          # Error handling best practices
├── filtering/               # Query filtering techniques
├── kafka/                   # Event-driven architecture with Kafka
├── middleware/              # Custom middleware implementation
├── pagination/              # Pagination strategies
├── payment_and_subscription/# Payment processing & subscriptions
├── postgre_sql/             # SQL database integration with SQLAlchemy
├── pydantic/                # Data validation with Pydantic
├── redis/                   # Caching & rate limiting with Redis
└── README.md                # This file
```

---

## 📖 Module Descriptions

### 🔐 **auth_api/** - Authentication Foundation
**What you'll learn:** Basic authentication flow with FastAPI

**Key files:**
- `app/main.py` - FastAPI application setup
- `app/auth.py` - Authentication router
- `app/schemas.py` - Request/response validation
- `app/security.py` - Password hashing and JWT utilities

**Key concepts:**
- User registration and login
- Password hashing (bcrypt)
- Basic JWT token generation
- Protected routes with token validation

**How to run:**
```bash
cd auth_api
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
# Visit http://localhost:8000/docs
```

---

### 📊 **postgre_sql/** - Database Integration
**What you'll learn:** SQL database setup, SQLAlchemy ORM, and database operations

**Key files:**
- `models.py` - SQLAlchemy ORM models
- `database.py` - Database connection and session management
- `schemas.py` - Pydantic schemas for validation
- `main.py` - CRUD endpoints

**Key concepts:**
- Database connection pooling
- ORM model definitions
- Transaction management
- Foreign keys and relationships
- Error handling for database operations

**How to run:**
```bash
cd postgre_sql
docker-compose up    # Starts PostgreSQL
python main.py       # In another terminal
```

---

### 🔗 **crud_api/** - Complete CRUD with Database & Auth
**What you'll learn:** Combining authentication with full CRUD operations on a database

**Key files:**
- `models.py` - Database models
- `crud.py` - CRUD operations
- `dependencies.py` - Dependency injection helpers
- `security.py` - JWT and auth utilities
- `main.py` - API endpoints

**Key concepts:**
- Secure CRUD operations
- Role-based access control (RBAC)
- Dependency injection for database sessions
- Protected endpoints with user context

**How to run:**
```bash
cd crud_api
docker-compose up
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

---

### 📄 **pydantic/** - Data Validation
**What you'll learn:** Input validation, serialization, and schema definition with Pydantic

**Key concepts:**
- Request/response models
- Field validation (min, max, regex patterns)
- Custom validators
- Nested models
- JSON schema generation

---

### 📍 **pagination/** - Pagination Strategies
**What you'll learn:** Implementing offset-limit pagination for large datasets

**Key files:**
- `main.py` - Pagination endpoint

**Example:**
```python
# Endpoint: GET /users?page=1&limit=10
# Returns:
{
    "page": 1,
    "limit": 10,
    "total": 100,
    "next_page": 2,
    "prev_page": null,
    "data": [...]
}
```

**Key concepts:**
- Offset-limit pagination
- Next/previous page calculation
- Query parameter validation with `Query`

---

### 🔍 **filtering/** - Advanced Query Filtering
**What you'll learn:** Implementing dynamic filtering on API endpoints

**Key concepts:**
- String search/contains filtering
- Case-insensitive matching
- Multiple field filtering
- Combining filtering with pagination

---

### 🏷️ **api_versioning/** - Version Management
**What you'll learn:** Maintaining multiple API versions simultaneously

**Key files:**
- `v1_offset_pagination.py` - Version 1 with offset pagination
- `v2.py` - Version 2 with potentially different schema

**Key concepts:**
- URL-based versioning (`/api/v1/`, `/api/v2/`)
- Using APIRouter with prefix
- Backward compatibility
- Gradual API evolution

**Example:**
```python
router_v1 = APIRouter(prefix="/api/v1", tags=["v1"])
# Endpoints registered under /api/v1/*
```

---

### 🔌 **middleware/** - Custom HTTP Middleware
**What you'll learn:** Implementing middleware for cross-cutting concerns

**Key files:**
- `main.py` - Custom middleware implementation

**Key concepts:**
- Request/response interception
- Rate limiting per client IP
- Request logging
- Execution time tracking
- Custom headers manipulation

---

### 💾 **redis/** - Caching & Rate Limiting
**What you'll learn:** Performance optimization with Redis

**Key files:**
- `cache.py` - Cache-aside pattern implementation
- `rate_limiter.py` - Rate limiting logic
- `redis_client.py` - Redis connection management
- `main.py` - API with caching and rate limiting

**Key concepts:**
- Cache-aside pattern (lazy loading)
- Cache invalidation strategies
- Rate limiting by client IP
- HTTP caching headers
- Redis data expiration (TTL)

**How to run:**
```bash
cd redis
docker-compose up
pip install -r requirements.txt
python -m uvicorn main:app --reload
```

---

### 🎯 **dependency_injection/** - DI Patterns
**What you'll learn:** Advanced dependency injection in FastAPI

**Key concepts:**
- Constructor-based injection
- Function parameter injection
- Dependency hierarchy
- Service locator pattern
- Testing with mock dependencies

---

### ⚠️ **Error_handling/** - Exception Management
**What you'll learn:** Comprehensive error handling strategies

**Key concepts:**
- HTTP exception mapping
- Custom exception classes
- Error response formatting
- Validation error handling
- Logging and error tracking

---

### 💬 **kafka/** - Event-Driven Architecture
**What you'll learn:** Asynchronous event processing with message queues

**Key files:**
- `order_service.py` - Kafka producer for order events
- `email_service.py` - Kafka consumer for email processing

**Key concepts:**
- Publish-subscribe pattern
- Event serialization (JSON)
- Asynchronous processing
- Multiple consumers
- Message ordering guarantees

**How to run:**
```bash
cd kafka
docker-compose up              # Start Kafka and Zookeeper
python order_service.py &      # Producer
python email_service.py        # Consumer
# Send POST request to producer to trigger events
```

---

### 💳 **payment_and_subscription/** - Complex Business Logic
**What you'll learn:** Implementing subscription and payment workflows

**Key files:**
- `models.py` - Payment and subscription models
- `database.py` - Database setup
- `rabbitmq.py` - Message queue integration
- `worker.py` - Background job processor
- `main.py` - API endpoints

**Key concepts:**
- Subscription state management
- Payment processing integration
- Background task queuing (RabbitMQ)
- Worker pattern for async jobs
- Webhook handling for payment updates

**How to run:**
```bash
cd payment_and_subscription
docker-compose up
python create_tables.py        # Initialize database
python -m uvicorn main:app --reload  # API server
python worker.py               # Background worker (separate terminal)
```

---

## 🎓 Learning Path

### Beginner → Intermediate → Advanced

1. **Start here:**
   - `pagination/` - Understand API pagination basics
   - `filtering/` - Add filtering to queries
   - `pydantic/` - Master data validation

2. **Build on the foundation:**
   - `auth_api/` - Implement authentication
   - `postgre_sql/` - Work with databases
   - `middleware/` - Handle cross-cutting concerns

3. **Combine concepts:**
   - `crud_api/` - Full CRUD with auth
   - `api_versioning/` - Manage API evolution
   - `Error_handling/` - Production-ready error handling

4. **Advanced patterns:**
   - `redis/` - Performance optimization
   - `kafka/` - Event-driven systems
   - `payment_and_subscription/` - Complex workflows

---

## 🔧 Common Setup

### Docker Compose Services

Several modules use Docker Compose for external services. Common services include:

- **PostgreSQL** - SQL database
- **Redis** - In-memory cache and rate limiting
- **Kafka** - Message broker
- **RabbitMQ** - Task queue

### General Commands

```bash
# Start services in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Remove volumes (WARNING: deletes data)
docker-compose down -v
```

### Testing an Endpoint

Using curl or FastAPI's built-in Swagger UI:

```bash
# Start any service and navigate to:
http://localhost:8000/docs

# Or use curl:
curl http://localhost:8000/users?page=1&limit=10
```

---

## 💡 Key Takeaways

- **FastAPI**: Modern, fast web framework with automatic API documentation
- **SQLAlchemy**: Powerful ORM for database operations
- **Pydantic**: Type-safe data validation
- **Docker**: Containerization for consistent environments
- **Async/Await**: Python's asynchronous programming model
- **Middleware**: Request/response interception and modification
- **Message Queues**: Decoupling services (Kafka, RabbitMQ)
- **Caching**: Performance optimization with Redis
- **Authentication**: Secure user identity management with JWT

---

## 📝 Notes

- Each module is self-contained and can be run independently
- Remember to install dependencies before running each module
- Docker services require Docker and Docker Compose to be installed
- FastAPI automatically generates API documentation at `/docs` (Swagger UI)
- Use `--reload` flag when running with uvicorn for development

---

## 🤝 Contributing

As you progress through this learning repository, feel free to:
- Extend existing modules with new features
- Add comments explaining key concepts
- Create additional examples
- Document any issues or improvements

Happy learning! 🚀