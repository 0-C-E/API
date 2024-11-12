# 0 C.E. API

This is the backend API for the **0 C.E.** game, providing essential services and data to support game functionality. The API is currently in development and will expand with more endpoints and features over time.

## Table of Contents
- [Overview](#overview)
- [Getting Started](#getting-started)
- [Endpoints](#endpoints)
- [Response Structure](#response-structure)
- [Running in Docker](#running-in-docker)
- [Future Development](#future-development)

## Overview

The 0 C.E. API is built with Flask and uses JSON for data communication. Initially, it provides a basic endpoint for retrieving the server time, but it will expand as more game functionality is implemented.

## Getting Started

To run the API locally, you’ll need:
- **Docker** to build and run the application in a container.

### Setup Steps

1. **Build the Docker Image**:
   ```bash
   docker build -t 0ce-flask-api .
   ```
2. **Run the Docker Container**:
   ```bash
   docker run -p 5000:5000 --name 0ce-flask-api 0ce-flask-api
   ```
3. **Access the API**:
   Open your browser or API client to `http://localhost:5000`.

## Endpoints

### 1. `/time` - Retrieve Server Time

- **Description**: This endpoint returns the current server time.
- **Method**: `GET`
- **URL**: `/time`
- **Response**:
  ```json
  {
    "status": "success",
    "data": {
      "server_time": "2023-12-01T12:34:56Z"
    }
  }
  ```
  
  **Sample Response (Error)**:
  ```json
  {
    "status": "error",
    "message": "Resource not found"
  }
  ```
  
**Note**: Additional endpoints will be added as the game develops.

## Response Structure

To maintain consistency across responses, all data responses will follow a standard JSON format:
- **Success**:
  ```json
  {
    "status": "success",
    "data": { ... }
  }
  ```
- **Error**:
  ```json
  {
    "status": "error",
    "message": "Error message here"
  }
  ```

This structure allows easy parsing of successful responses and clear indication of errors.

## Running in Docker

The API is designed to run within a Docker container. Here’s a breakdown of the Dockerfile configuration and commands for running the container.

### Dockerfile Configuration

The [Dockerfile](Dockerfile) uses the official `python:3.13-slim` image and installs dependencies from `requirements.txt`. A health check verifies the container’s status every 30 seconds.

### Running the Container

To run the container, expose it on port 5000:
```bash
docker run -p 5000:5000 0ce-flask-api
```

Access the API via `http://localhost:5000`.

## Future Development

Planned API enhancements:
- **User Authentication**: Implementing a secure user authentication system.
- **Additional Endpoints**: To support game features like city management, alliances, resources, and combat.
- **Error Handling and Logging**: Structured error codes and enhanced logging for debugging and monitoring.
- **API Versioning**: To support backward compatibility in future versions.
