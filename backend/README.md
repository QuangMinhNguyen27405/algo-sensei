# Algo Sensei Backend

FastAPI backend for the Algo Sensei application.

## Getting Started

### Prerequisites

- Python 3.11+
- Poetry

### Installation

1. Install dependencies:

```bash
poetry install
```

2. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your configuration
```

### Running the Application

**Development mode:**

```bash
uvicorn app.main:app --reload --log-config=json_config/log_conf.dev.yaml
```

**Production mode:**

```bash
uvicorn app.main:app --log-config=json_config/log_conf.prod.yaml
```

The API will be available at `http://127.0.0.1:8000`

### Running Tests

```bash
poetry run pytest
```
