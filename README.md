# Docs Backend v0.1

A FastAPI-based backend for a document management system. This application provides user authentication, document management (upload, retrieval, updates, deletion), and automated text extraction from PDF and text files.

## Key Features

*   **FastAPI Framework:** High-performance, easy-to-learn, fast to code, ready for production.
*   **Authentication:** Secure user authentication using JWT (JSON Web Tokens) with `python-jose` and password hashing with `passlib`.
*   **Database Integration:** PostgreSQL database using SQLAlchemy ORM for robust data management.
*   **Document Processing:**
    *   File upload handling.
    *   Automated text extraction from `.pdf` and `.txt` files using `pypdf`.
    *   CRUD operations for document metadata.
*   **Docker Support:** Docker Compose configuration for easy database setup.

## Prerequisites

*   **Python 3.9+**
*   **Docker & Docker Compose** (for running the PostgreSQL database)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Environment Configuration

Create a `.env` file in the root directory. You can copy the example below:

```bash
# .env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/docsdb
SECRET_KEY=your-secret-key-here
```

*   `DATABASE_URL`: Connection string for the PostgreSQL database. The default matches the `docker-compose.yml` configuration.
*   `SECRET_KEY`: Secret key for JWT encoding/decoding. If not set, it defaults to `dev-secret-key`.

### 3. Start the Database

Use Docker Compose to start the PostgreSQL container:

```bash
docker-compose up -d
```

This will start a PostgreSQL instance on port 5432 with the credentials specified in `docker-compose.yml`.

### 4. Install Dependencies

It is recommended to use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Install the required Python packages:

```bash
pip install -r requirements.txt
```

### 5. Run the Application

Start the FastAPI server using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The application will start at `http://localhost:8000`.

## API Documentation

FastAPI automatically generates interactive API documentation. Once the server is running, you can access it at:

*   **Swagger UI:** [http://localhost:8000/docs](http://localhost:8000/docs)
*   **ReDoc:** [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Project Structure

```
.
├── app/
│   ├── api/            # API route handlers (endpoints)
│   ├── core/           # Core configuration, security, and utility logic
│   ├── db/             # Database connection and session management
│   ├── models/         # SQLAlchemy database models
│   ├── schemas/        # Pydantic models for request/response schemas
│   └── main.py         # Application entry point and configuration
├── docker/             # Docker related files
├── docker-compose.yml  # Docker Compose configuration for services (DB)
├── requirements.txt    # Python dependencies
└── .env                # Environment variables (not committed)
```
