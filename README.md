# Todo List Application with FastAPI, MongoDB, and Docker

A modern, containerized todo list application with a FastAPI backend, MongoDB database, and a responsive frontend.


## Demo
![demo](demo.png)

## 🚀 Features

- **Full-stack Todo Application**: Create, read, delete tasks
- **MongoDB Persistence**: Tasks are stored in MongoDB database
- **Docker Containerization**: All services run in Docker containers
- **FastAPI Backend**: Modern Python async API with automatic docs
- **Responsive Frontend**: Clean, mobile-friendly UI
- **Health Monitoring**: Built-in health checks for all services

## 🏗️ Architecture

```
└── 📁backend (FastAPI + MongoDB)
└── 📁frontend (Static HTML/CSS/JS)
└── 📁mongodb (MongoDB configuration)
└── docker-compose.yml
```

## 🛠️ Technologies

- **Backend**: FastAPI, Python 3.12, Motor (async MongoDB driver)
- **Database**: MongoDB 7.0.12
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Web Server**: Nginx
- **Containerization**: Docker, Docker Compose
- **Package Management**: Python Poetry (pyproject.toml)

## 📋 Prerequisites

- [Docker](https://docs.docker.com/get-docker/) and [Docker Compose](https://docs.docker.com/compose/install/)
- Git (for cloning the repository)
- At least 2GB of free RAM

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd todo-fastapi-mongodb
```

### 2. Set Up Environment Variables

Copy the example environment files and update them if needed:

```bash
# Backend environment
cp backend/.env.example backend/.env

# MongoDB environment
cp mongodb/.env.example mongodb/.env
```

The default values should work for local development.

### 3. Build and Run with Docker Compose

```bash
docker-compose up --build
```

This command will:
- Build Docker images for all services
- Start MongoDB, FastAPI backend, and frontend containers
- Set up a Docker network for inter-container communication
- Mount persistent volumes for MongoDB data

### 4. Access the Application

Once all containers are running, access the application at:

- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **MongoDB**: localhost:27017 (use MongoDB Compass or similar tool)


## API Endpoints

### Base URL: `http://localhost:8000` or `http://backend:8000` (in Docker)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | API information |
| GET | `/health` | Health check with MongoDB status |
| GET | `/tasks` | Get all tasks |
| POST | `/tasks` | Create a new task |
| DELETE | `/tasks/{id}` | Delete a specific task |
| DELETE | `/tasks` | Delete all tasks |
| PUT | `/tasks/{id}` | Update a task (optional) |



## 📁 Project Structure

```
├── backend/                    # FastAPI backend
│   ├── src/mysite/            # Python package
│   │   ├── __init__.py        # Package initialization
│   │   └── main.py            # FastAPI application
│   ├── .env                   # Backend environment variables
│   ├── .env.example           # Example environment variables
│   ├── Dockerfile             # Backend Docker configuration
│   ├── pyproject.toml         # Python dependencies and metadata
│   └── requirements.txt       # Python package requirements
│
├── frontend/                  # Frontend application
│   ├── static/                # Static files
│   │   └── index.html         # Main HTML file with CSS/JS
│   └── Dockerfile             # Frontend Docker configuration
│
├── mongodb/                   # MongoDB configuration
│   ├── .env                   # MongoDB environment variables
│   └── .env.example           # Example MongoDB environment
│
├── docker-compose.yml         # Multi-container orchestration
└── README.md                  # This file
```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```bash
MONGODB_CONNECTION_STRING=mongodb://admin:password123@mongodb:27017/todoapp?authSource=admin
```

#### MongoDB (.env)
```bash
MONGO_INITDB_ROOT_USERNAME=admin
MONGO_INITDB_ROOT_PASSWORD=password123
MONGO_INITDB_DATABASE=todoapp
```

### Docker Compose Services

| Service | Port | Description |
|---------|------|-------------|
| backend | 8000 | FastAPI REST API |
| frontend | 5000 | Nginx web server with frontend |
| mongodb | 27017 | MongoDB database |




## Acknowledgments

- FastAPI for the excellent Python web framework
- MongoDB for the flexible document database
- Docker for containerization technology
- All open-source contributors


---

**Happy Todo-ing!**