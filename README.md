# Mockuper: See Your Customized Shirt Before You Order!

## Table of Contents

- [What Does It Do?](#what-does-it-do)
- [Example Outputs](#example-outputs)
- [API Endpoints](#api-endpoints)
- [Documentation Endpoints](#documentation-endpoints)
- [Technologies Used](#technologies-used)

## What Does It Do?

Mockuper is a Django-based REST API that generates customized shirt mockups by overlaying text onto shirt templates. The project uses **Pillow** for image processing and **Celery** for asynchronous task execution, allowing users to preview their custom shirt designs before ordering.

## Example Outputs

### Example 1
**Request Body:** `{"text": "Python", "font": "audiowide"}`
![Example 1](https://github.com/MohammadYeganeFar/Mockuper/blob/main/example_outputs/generated_image878.png?raw=true)

### Example 2
**Request Body:** `{"text": "Hello world!", "font": "roboto"}`
![Example 2](https://github.com/MohammadYeganeFar/Mockuper/blob/main/example_outputs/generated_image14.png?raw=true)

### Example 3
**Request Body:** `{"text": "Java", "font": "bungee"}`
![Example 3](https://github.com/MohammadYeganeFar/Mockuper/blob/main/example_outputs/generated_image242.png?raw=true)

### Example 4
**Request Body:** `{"text": "LOVING BLACK", "font": "arial"}`
![Example 4](https://github.com/MohammadYeganeFar/Mockuper/blob/main/example_outputs/generated_image515.png?raw=true)

## API Endpoints

### 1. Generate Mockup

**Endpoint:** `POST /api/v1/mockups/generate/`

Generates customized shirt mockups with the provided text and optional font. The endpoint triggers a group of Celery tasks that process shirt images in the background, overlay the text, and save the results to the database.

**Available Fonts:**
- `roboto` (default)
- `arial`
- `bungee`
- `audiowide`

**Request Body:**
```json
{
    "text": "python",
    "font": "audiowide"
}
```

**Response:**
```json
{
    "task_uuid": "4650538c-18dc-4b03-8318-76e589c5b791",
    "status": "PENDING",
    "message": "Image generation started"
}
```

### 2. Get Task Status

**Endpoint:** `GET /api/v1/tasks/<task_uuid>/`

Retrieves the status and results of an asynchronous task by its UUID.

**Example URL:** `api/v1/tasks/7ee0785b-643b-4bf6-b4de-157a5d614245/`

**Response:**
```json
{
    "task_uuid": "7ee0785b-643b-4bf6-b4de-157a5d614245",
    "status": "SUCCESS",
    "results": [
        {
            "image_url": "http://127.0.0.1:8000/media/mockups/generated_image31.png",
            "created_at": "2025-11-03T14:58:11.083379Z"
        },
        {
            "image_url": "http://127.0.0.1:8000/media/mockups/generated_image475.png",
            "created_at": "2025-11-03T14:58:11.098406Z"
        },
        {
            "image_url": "http://127.0.0.1:8000/media/mockups/generated_image190.png",
            "created_at": "2025-11-03T14:58:11.134344Z"
        },
        {
            "image_url": "http://127.0.0.1:8000/media/mockups/generated_image960.png",
            "created_at": "2025-11-03T14:58:11.139082Z"
        }
    ]
}
```

### 3. List Mockups

**Endpoint:** `GET /api/v1/mockups/`

Retrieves a paginated list of previously generated mockups with support for search and filtering.

**Query Parameters:**
- `q` - Search query (searches in text field)
- `page` - Page number for pagination
- `page_size` - Number of results per page
- `from` and `to` - Filter by creation date (ISO 8601 format)

**Example URL:** `api/v1/mockups/?q=python&page=2&page_size=2&from=2025-11-03T12:26:25Z`

**Response:**
```json
{
    "count": 20,
    "next": "http://localhost:8000/api/v1/mockups/?from=2025-11-03T12%3A26%3A25Z&page=3&page_size=3&q=python",
    "previous": "http://localhost:8000/api/v1/mockups/?from=2025-11-03T12%3A26%3A25Z&page_size=3&q=python",
    "results": [
        {
            "id": 81,
            "text": "python",
            "url": "http://127.0.0.1:8000/media/mockups/generated_image967.png",
            "created_at": "2025-11-03T13:45:36.433230Z"
        },
        {
            "id": 80,
            "text": "python",
            "url": "http://127.0.0.1:8000/media/mockups/generated_image645.png",
            "created_at": "2025-11-03T13:37:16.645511Z"
        },
        {
            "id": 79,
            "text": "python",
            "url": "http://127.0.0.1:8000/media/mockups/generated_image86.png",
            "created_at": "2025-11-03T13:37:16.633188Z"
        }
    ]
}
```

## Documentation Endpoints

### API Schema

- **`GET /api/schema/`** - Downloads API documentation in YAML format
- **`GET /api/schema/swagger-ui/`** - Interactive Swagger UI documentation
- **`GET /api/schema/redoc/`** - ReDoc documentation interface

## Technologies Used

- **Celery** - Distributed task queue for running background jobs
- **Redis** - Message broker and result backend for Celery
- **Pillow** - Image processing library for overlaying text on shirt templates
- **Django** - Web framework implementing the MVT (Model-View-Template) architecture
- **Django REST Framework** - Toolkit for building RESTful APIs, including serialization, pagination, and testing utilities
- **Docker** - Containerization platform for packaging and deploying the application
- **PostgreSQL** - Relational database management system
