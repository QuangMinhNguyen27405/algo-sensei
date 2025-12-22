# Backend Tests

This folder contains tests for the authentication endpoints and service layer.

## Running tests

Using Poetry in the backend folder:

```bash
cd backend
poetry install --with dev
poetry run pytest -q
```

Or using a system-wide pytest:

```bash
cd backend
pytest -q
```
