# WorkoutHub

A comprehensive workout tracking and analytics platform built with FastAPI and PostgreSQL.

## 🏋️ Features

- **Exercise Database**: Comprehensive library of exercises with muscle group targeting
- **Equipment Tracking**: Support for gym equipment and bodyweight exercises
- **Workout Logging**: Record sets with weight, reps, RPE, duration, and notes
- **Hierarchical Muscle Groups**: Organized muscle group classification
- **Progress Analytics**: Track performance over time
- **Data Import**: Import workouts from Strong app CSV exports

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL 12+
- Virtual environment (recommended)

### Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd workoutHub
```

2. Create and activate virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up environment variables:

```bash
cp .env.example .env
# Edit .env with your database credentials
```

5. Start the API server:

```bash
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

## 📊 API Documentation

The API provides automatic documentation at:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Data Format

The API returns data in **MessagePack** format for efficient serialization. All datetime fields are serialized as ISO 8601 strings.

### Key Endpoints

- `GET /sets/` - Get all workout sets
- `GET /exercises/` - Get all exercises
- `GET /equipment/` - Get all equipment
- `GET /muscle-groups/` - Get muscle groups
- `GET /sets/exercises/{exercise_id}` - Get sets for specific exercise

## 🗄️ Database Schema

### Core Models

- **Set**: Individual workout sets with weight, reps, RPE
- **Exercise**: Exercise definitions with muscle group targeting
- **Equipment**: Gym equipment and bodyweight options
- **MuscleGroup**: Hierarchical muscle group organization

### Relationships

- Sets belong to exercises and optionally use equipment
- Exercises target primary muscle groups and optional secondary groups
- Muscle groups can have parent-child relationships

## 🔧 Development

### Project Structure

```
workoutHub/
├── backend/
│   ├── models/          # SQLModel definitions
│   ├── routers/         # FastAPI route handlers
│   ├── logger/          # Logging utilities
│   └── utils/           # Helper functions
├── converter/           # Data import utilities
├── data/               # Sample data and exports
└── requirements.txt    # Python dependencies
```

### Running Tests

```bash
# Run tests (when implemented)
pytest
```

### Database Migrations

The application automatically creates tables on startup. For production, consider using Alembic for migrations.

## 📈 Data Import

### Strong App CSV Import

Import your workout history from Strong app:

```python
from converter.strong_csv import import_strong_csv
import_strong_csv('path/to/strong-export.csv')
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support, email support@workouthub.com or open an issue on GitHub.
