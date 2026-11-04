
# Online Store – Product Service

## 1. Project Overview

The Product Service is a RESTful microservice developed as part of an Online Store application.

It manages product-related operations, including creating, retrieving, updating, changing product status, and deleting products.

The service is built using Python and FastAPI, with PostgreSQL as the database.

### Key Features

- Create a new product.
- Retrieve all products.
- Retrieve a product by ID.
- Update existing product details.
- Enable or disable a product.
- Delete a product.
- Pagination, filtering, and sorting.
- Input validation and standardized error responses.
- Duplicate product name validation.
- Database migration management using Alembic.
- Unit testing using pytest.

## 2. Technology Stack

| Technology | Purpose                                 |
| ---------- | --------------------------------------- |
| Python     | Programming language                    |
| FastAPI    | REST API framework                      |
| PostgreSQL | Relational database                     |
| SQLAlchemy | ORM and database operations             |
| Alembic    | Database migrations                     |
| Pydantic   | Request validation and response schemas |
| Pytest     | Unit testing                            |
| Uvicorn    | ASGI application server                 |

## 3. Project Structure

```text
product-service/
│
├── app/
│   ├── core/
│   │   ├── config.py
│   │   └── exceptions.py
│   │
│   ├── models/
│   │   └── product.py
│   │
│   ├── repositories/
│   │   └── product_repository.py
│   │
│   ├── routes/
│   │   └── product_routes.py
│   │
│   ├── schemas/
│   │   ├── product.py
│   │   └── error_schema.py
│   │
│   ├── services/
│   │   └── product_service.py
│   │
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── tests/
│   ├── __init__.py
│   └── test_product_service.py
│
├── .env
├── .env.example
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

## 4. Prerequisites

Make sure the following software is installed:

- Python 3.10 or above.
- PostgreSQL.
- Visual Studio Code or another code editor.
- Git.
- pip (Python package manager).

## 5. Installation and Configuration

### Step 1: Clone the repository

```bash
git clone <repository-url>
```

Navigate to the Product Service directory:

```bash
cd product-service
```

### Step 2: Create a virtual environment

```bash
python -m venv .venv
```

Activate the virtual environment.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### Step 3: Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure environment variables

Create a `.env` file in the project root.

Example:

```env
DATABASE_URL=postgresql+psycopg://username:password@localhost:5432/product_db
```

Replace the username and password with your PostgreSQL credentials.

Create the PostgreSQL database named `product_db` before running migrations.

**Note:** Never commit the actual `.env` file to Git. Use `.env.example` to share placeholder configuration.

## 6. Database Migrations

Alembic is used to manage database schema changes.

### Apply migrations

Run:

```bash
alembic upgrade head
```

This applies all available migrations to the database.

### Check migration history

```bash
alembic history
```

### Check the current migration

```bash
alembic current
```

Migration scripts are maintained inside:

```text
alembic/versions/
```

## 7. Running the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The application will run at:

```text
http://127.0.0.1:8000
```

### Swagger UI Documentation

FastAPI automatically generates interactive API documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

### ReDoc Documentation

Alternative API documentation is available at:

```text
http://127.0.0.1:8000/redoc
```

The OpenAPI specification can be accessed at:

```text
http://127.0.0.1:8000/openapi.json
```

## 8. API Endpoints

Base URL:

```text
http://127.0.0.1:8000/api/v1
```

| HTTP Method | Endpoint                          | Description                 |
| ----------- | --------------------------------- | --------------------------- |
| POST        | `/products`                     | Create a product            |
| GET         | `/products`                     | Retrieve all products       |
| GET         | `/products/{product_id}`        | Retrieve a product by ID    |
| PUT         | `/products/{product_id}`        | Update product details      |
| PATCH       | `/products/{product_id}/status` | Enable or disable a product |
| DELETE      | `/products/{product_id}`        | Delete a product            |

## 9. Example API Requests

### 9.1 Create Product

**POST**

```text
/api/v1/products
```

Request body:

```json
{
    "name": "Laptop",
    "description": "Business laptop",
    "price": 55000,
    "quantity": 10,
    "category": "Electronics"
}
```

Expected result: Product created successfully.

### 9.2 Retrieve All Products

**GET**

```text
/api/v1/products
```

Example with pagination:

```text
/api/v1/products?skip=0&limit=10
```

Example with filters:

```text
/api/v1/products?category=Electronics&minPrice=10000&maxPrice=60000
```

Example with sorting:

```text
/api/v1/products?sortBy=price_asc
```

### 9.3 Retrieve Product by ID

**GET**

```text
/api/v1/products/1
```

Retrieves the product with ID 1.

### 9.4 Update Product

**PUT**

```text
/api/v1/products/1
```

Example request body:

```json
{
    "name": "Updated Laptop",
    "description": "Updated business laptop",
    "price": 60000,
    "quantity": 15,
    "category": "Electronics",
    "status": "Active"
}
```

### 9.5 Update Product Status

**PATCH**

```text
/api/v1/products/1/status
```

Example request body:

```json
{
    "status": "Inactive"
}
```

### 9.6 Delete Product

**DELETE**

```text
/api/v1/products/1
```

Deletes the product with ID 1.

## 10. Error Handling

The service uses standardized error responses.

Example: Product not found.

```json
{
    "timestamp": "2026-10-27T10:15:30Z",
    "status": 404,
    "error": "Not Found",
    "message": "Product not found",
    "path": "/api/v1/products/999",
    "details": []
}
```

Common HTTP status codes:

| Status Code | Description                     |
| ----------- | ------------------------------- |
| 200         | Successful request              |
| 201         | Resource created, if configured |
| 400         | Bad Request                     |
| 404         | Product not found               |
| 409         | Duplicate product name          |
| 422         | Validation error                |
| 500         | Internal Server Error           |

## 11. Running Unit Tests

Unit tests are implemented using pytest.

Make sure the virtual environment is activated.

Run all tests:

```bash
python -m pytest -v
```

The tests verify service-layer functionality without requiring the Uvicorn server to run.

Mock database objects are used to isolate the service logic from the actual database.

## 12. Architecture and Design

The Product Service follows a layered architecture.

### Controller / Routes Layer

- Handles incoming HTTP requests.
- Validates and forwards request data.
- Returns appropriate HTTP responses.

### Service Layer

- Implements business logic.
- Handles product-related operations.
- Performs duplicate product name checks.
- Handles product-not-found scenarios.

### Repository Layer

- Handles database queries.
- Performs database access operations.
- Supports filtering, sorting, and pagination.

### Models Layer

- Defines SQLAlchemy database models.
- Represents product records in PostgreSQL.

### Schemas Layer

- Defines Pydantic request and response schemas.
- Validates incoming data.
- Controls API data structures.

## 13. Day 1 Design Note

The Product Service was designed to manage product information independently within the Online Store microservices architecture.

### Main Endpoints

- POST `/api/v1/products`
- GET `/api/v1/products`
- GET `/api/v1/products/{product_id}`
- PUT `/api/v1/products/{product_id}`
- PATCH `/api/v1/products/{product_id}/status`
- DELETE `/api/v1/products/{product_id}`

### Product Data Fields

| Field       | Data Type | Description                |
| ----------- | --------- | -------------------------- |
| id          | Integer   | Auto-generated primary key |
| name        | String    | Product name               |
| description | String    | Product description        |
| price       | Decimal   | Product price              |
| quantity    | Integer   | Available quantity         |
| category    | String    | Product category           |
| status      | Enum      | Active or Inactive         |
| createdAt   | Timestamp | Creation timestamp         |
| updatedAt   | Timestamp | Last update timestamp      |

### Design Principles

1. **Layered Architecture:** Separate routes, services, and repositories.
2. **Data Validation:** Validate incoming requests using Pydantic.
3. **Error Handling:** Return consistent error responses.
4. **Database Management:** Use PostgreSQL with SQLAlchemy and Alembic.
5. **Maintainability:** Keep business logic separate from HTTP and database access.
6. **Testing:** Use automated unit tests to verify service functionality.

---

## 14. Future Improvements

- Add integration tests for API endpoints.
- Add authentication and authorization.
- Add structured application logging.
- Add Docker support.
- Add CI/CD pipeline integration.
- Add API versioning and monitoring.

---

## 15. Author

Avinaash K P

Python Developer
