# WorkoutHub API Documentation

## Overview

The WorkoutHub API provides endpoints for managing workout data including exercises, sets, equipment, and muscle groups. All responses are returned in MessagePack format for efficient data transfer.

## Base URL

```plaintext
http://localhost:8000
```

## Authentication

Currently no authentication is required (development mode).

## Response Format

All API responses use **MessagePack** binary serialization format with the content type `application/msgpack`.

### DateTime Serialization

All datetime fields are serialized as ISO 8601 strings:

```plaintext
"2025-06-20T10:30:00"
```

## Core Endpoints

### Sets

#### GET /sets/

Returns all workout sets with enriched data including exercise names and muscle group information.

**Response Schema:**

```json
[
  {
    "id": 1,
    "exercise_id": 1,
    "equipment_id": 1,
    "date": "2025-06-20T10:30:00",
    "weight": 100.0,
    "reps": 10,
    "rpe": 8,
    "notes": "Felt strong today",
    "duration": null,
    "distance": null,
    "exercise_name": "Bench Press",
    "primary_muscle_group_name": "Chest",
    "main_muscle_group": "Chest"
  }
]
```

#### GET /sets/{set_id}

Returns a specific workout set by ID.

#### GET /sets/exercises/{exercise_id}

Returns all sets for a specific exercise.

#### GET /sets/exercises/equipment/{exercise_id}/{equipment_id}

Returns all sets for a specific exercise using specific equipment.

### Exercises

#### GET /exercises/

Returns all exercises with their muscle group and equipment relationships.

**Response Schema:**

```json
[
  {
    "id": 1,
    "name": "Bench Press",
    "type": "Strength",
    "primary_muscle_group_id": 1
  }
]
```

#### GET /exercises/{exercise_id}

Returns a specific exercise by ID.

### Equipment

#### GET /equipment/

Returns all available equipment.

**Response Schema:**

```json
[
  {
    "id": 1,
    "name": "Barbell"
  }
]
```

#### GET /equipment/{equipment_id}

Returns specific equipment by ID.

### Muscle Groups

#### GET /muscle-groups/

Returns all muscle groups with hierarchical relationships.

**Response Schema:**

```json
[
  {
    "id": 1,
    "name": "Chest",
    "parent_id": null
  }
]
```

#### GET /muscle-groups/{muscle_group_id}

Returns a specific muscle group by ID.

## Data Models

### Set

- `id`: Unique identifier
- `exercise_id`: Reference to exercise
- `equipment_id`: Optional reference to equipment
- `date`: When the set was performed
- `weight`: Weight used (kg)
- `reps`: Number of repetitions
- `rpe`: Rate of Perceived Exertion (1-10)
- `notes`: Optional notes
- `duration`: Duration in seconds (for cardio)
- `distance`: Distance in kilometers (for cardio)

### Exercise

- `id`: Unique identifier
- `name`: Exercise name
- `type`: Exercise type (Strength/Cardio/Flexibility)
- `primary_muscle_group_id`: Primary muscle group targeted

### Equipment

- `id`: Unique identifier
- `name`: Equipment name

### MuscleGroup

- `id`: Unique identifier
- `name`: Muscle group name
- `parent_id`: Optional parent muscle group for hierarchy

## Error Responses

### 404 Not Found

```json
{
  "detail": "Resource not found"
}
```

### 422 Validation Error

```json
{
  "detail": [
    {
      "loc": ["body", "field_name"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

## Rate Limiting

No rate limiting is currently implemented.

## Changelog

### v0.1.0

- Initial API release
- Basic CRUD operations for all entities
- MessagePack response format
- Hierarchical muscle groups
- Exercise-equipment relationships
