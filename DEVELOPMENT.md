# Development Guide

## Setting Up Development Environment

### Prerequisites

- Python 3.12+
- PostgreSQL 12+
- Git
- Virtual environment tool (venv or conda)

### Local Development Setup

1. **Clone and setup repository:**

   ```bash
   git clone <repository-url>
   cd workoutHub
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Database setup:**

   ```bash
   # Create PostgreSQL database
   createdb workouthub_dev
   
   # Set environment variables
   export POSTGRES_USER=your_username
   export POSTGRES_PASSWORD=your_password
   export POSTGRES_HOST=localhost
   export POSTGRES_PORT=5432
   export POSTGRES_DB=workouthub_dev
   ```

3. **Run the application:**

   ```bash
   uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Code Organization

### Directory Structure

```plaintext
backend/
├── models/          # Database models and schemas
├── routers/         # API route handlers
├── logger/          # Logging configuration
├── utils/           # Utility functions
├── database.py      # Database connection and setup
├── main.py          # FastAPI application entry point
└── populate.py      # Database population scripts
```

### Coding Standards

- **Python Style**: Follow PEP 8
- **Docstrings**: Use Google-style docstrings
- **Type Hints**: Use type hints for all function parameters and return values
- **Error Handling**: Use proper HTTP status codes and FastAPI HTTPException

### Database Models

- Use SQLModel for all database models
- Include comprehensive docstrings with field descriptions
- Add validation constraints using Pydantic validators
- Use meaningful relationship names

### API Endpoints

- Include comprehensive docstrings
- Use proper HTTP methods (GET, POST, PUT, DELETE)
- Include response models for documentation
- Handle errors gracefully with appropriate status codes

## Testing

### Unit Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=backend
```

### Integration Tests

```bash
# Test API endpoints
pytest tests/test_api.py
```

### Manual Testing

Use the interactive API documentation at `http://localhost:8000/docs` for manual testing.

## Database Management

### Migrations

Currently, the application uses SQLModel's automatic table creation. For production, consider implementing Alembic migrations:

```bash
# Install Alembic
pip install alembic

# Initialize migrations
alembic init alembic

# Create migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head
```

### Data Population

Use the populate script to add initial data:

```python
from backend.populate import populate_db
populate_db()
```

## Performance Considerations

### Database Optimization

- Use database indexes for frequently queried fields
- Implement connection pooling for production
- Consider read replicas for analytics queries

### API Optimization

- Use MessagePack for efficient data serialization
- Implement caching for frequently accessed data
- Add request/response compression

## Debugging

### Logging

The application uses structured logging. Enable debug logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Database Queries

Enable SQL query logging:

```python
engine = create_engine(connection_string, echo=True)
```

## Contributing

### Code Review Checklist

- [ ] Code follows PEP 8 style guidelines
- [ ] All functions have type hints and docstrings
- [ ] Tests are included for new functionality
- [ ] Database models include proper validation
- [ ] API endpoints have comprehensive documentation
- [ ] Error handling is implemented
- [ ] Performance impact is considered

### Pull Request Process

1. Create feature branch from main
2. Implement changes with tests
3. Update documentation
4. Run linting and tests
5. Submit pull request with detailed description

## Troubleshooting

### Common Issues

1. **Database Connection Errors**
   - Check PostgreSQL is running
   - Verify connection parameters
   - Ensure database exists

2. **Import Errors**
   - Check virtual environment is activated
   - Verify all dependencies are installed
   - Check Python path configuration

3. **API Errors**
   - Check server logs for detailed error messages
   - Verify request format and parameters
   - Test with curl or API documentation interface
