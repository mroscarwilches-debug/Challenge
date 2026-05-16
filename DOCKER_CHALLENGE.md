# Docker Gym App Challenge

This is the next challenge for Oscar: Build a multi-layered gym app using Docker with database, microservices, and frontend.

## Overview

Create a gym weight converter app where users can:
- Add their name and weight (in kg or lb)
- Convert weights between kg and lb
- View all users and their weights
- Store data in a database

The app will have 3 layers:
1. Database layer (PostgreSQL)
2. Microservices layer (Python/Flask for API)
3. Frontend layer (simple web UI)

## Requirements

### Functional Requirements
- User management: add user with name and weight
- Weight conversion: kg ↔ lb
- View all users in a list
- Store users in database with id, name, weight
- Simple web interface

### Technical Requirements
- Use Docker and Docker Compose
- Microservices architecture
- Database persistence
- Unit tests for services
- Best practices for project structure
- Provide proof of running containers

## Architecture

### Suggested Layers
- **Database**: PostgreSQL container
- **API Service**: Python Flask app for user management and conversions
- **Frontend Service**: Simple HTML/CSS/JS web app

### Diagram
Create a simple architecture diagram showing:
- Frontend → API Service → Database
- Docker containers and their connections
- Data flow for user operations

## Development Phases

Divide the work into branches for review:

1. **Branch: feature/database-setup**
   - Set up PostgreSQL Docker container
   - Create database schema (users table)
   - Provide docker-compose.yml snippet

2. **Branch: feature/api-service**
   - Create Flask API service
   - Endpoints: GET/POST users, POST convert weight
   - Docker container for the service
   - Unit tests for API functions

3. **Branch: feature/frontend-ui**
   - Simple web interface (HTML/JS)
   - Forms for adding users and converting weights
   - Display user list
   - Docker container for frontend

4. **Branch: feature/docker-compose**
   - Combine all services in docker-compose.yml
   - Networking between containers
   - Volume mounts for data persistence

## Project Structure

Organize the repository like this:

```
gym-app/
├── docker-compose.yml
├── database/
│   ├── Dockerfile
│   ├── init.sql
│   └── ...
├── api/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   ├── tests/
│   └── ...
├── frontend/
│   ├── Dockerfile
│   ├── index.html
│   ├── app.js
│   └── ...
└── README.md
```

## Best Practices

- Use environment variables for configuration
- Add health checks to containers
- Write unit tests for conversion logic
- Use proper error handling
- Document API endpoints
- Keep containers lightweight

## Instructions for Oscar

1. Create the architecture diagram first
2. Set up each layer in separate branches
3. Test each service individually
4. Combine with docker-compose
5. Provide screenshots/logs of running containers
6. Write instructions for running the full app

## Running the App

Once complete, provide these commands:
- `docker-compose up -d` to start
- Access frontend at http://localhost:3000
- API at http://localhost:5000
- Proof: screenshots of UI, API responses, database contents

## Testing

- Unit tests for weight conversion functions
- API endpoint tests
- Integration tests for full flow

## Recommendations

- Use Python Flask for API (simple and familiar)
- PostgreSQL for database
- Nginx or simple HTTP server for frontend
- Docker networks for service communication
- Volumes for database persistence

This challenge will teach Docker, microservices, and full-stack development.