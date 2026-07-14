# Todo List API

This project is an implementation of the [Todo List API](https://roadmap.sh/projects/todo-list-api) project idea from **roadmap.sh**.

## Features

- **User Authentication**: Secure user registration and login using JWT (JSON Web Tokens) and bcrypt password hashing.
- **Todo Management**: Complete CRUD (Create, Read, Update, Delete) operations for to-do items.
- **Data Isolation**: Users can only access and manage their own to-do items.
- **Filtering & Pagination**: Retrieve to-do lists with pagination, completion status filtering, and title search.
- **Automated Testing**: Comprehensive unit and integration tests using `pytest` and an isolated in-memory database.

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL (Production/Dev), SQLite (Testing)
- **ORM**: SQLAlchemy
- **Package Manager**: [uv](https://github.com/astral-sh/uv)
- **Testing**: pytest, httpx

## Getting Started

### 1. Prerequisites

- Python 3.9+
- PostgreSQL server running locally or remotely
- `uv` package manager installed

### 2. Installation

Clone the repository:

```bash
git clone git@github.com:DoubleRu1/todo-list-api.git
cd todo-list-api
```

*(Dependencies will be automatically managed by `uv` when running the scripts).*

### 3. Environment Configuration

Create a `.env` file based on the provided example:

```bash
cp .env.example .env
```

Update the `SECRET_KEY` and the `DATABASE_URL` in your `.env` file with your actual PostgreSQL credentials.

### 4. Running the Server

Start the FastAPI server with hot-reload:

```bash
uv run uvicorn src.main:app --reload
```

Once running, open your browser and navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view and interact with the automatically generated Swagger API documentation.

## Testing

The project includes a robust suite of unit and integration tests. The tests automatically spin up an isolated SQLite in-memory database, so they won't affect your PostgreSQL data.

Run the tests using:

```bash
uv run python -m pytest -v
```
