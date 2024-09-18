# Cars API

This project is a FastAPI-based CRUD application, containerized using Docker, with PostgreSQL as the database. Dependencies are managed using Poetry.

## Table of Contents

- [Requirements](#requirements)
- [Project Setup](#project-setup)
  - [1. Clone the Repository](#1-clone-the-repository)
  - [2. Environment Variables](#2-environment-variables)
  - [3. Start the Application](#3-start-the-application)
- [Using the Application](#using-the-application)
- [Running Tests](#running-tests)
- [Linting the Code](#linting-the-code)
- [Makefile Commands](#makefile-commands)
- [Contributing](#contributing)
- [License](#license)

## Requirements

Ensure the following software is installed on your machine:

- **[Docker](https://www.docker.com/)**: for containerization.
- **[Poetry](https://python-poetry.org/)**: for managing Python dependencies. (no-actually-needed)
- **[Make](https://www.gnu.org/software/make/)**: for running `Makefile` commands.

## Project Setup

### 1. Clone the Repository (ssh)

```bash
git clone git@github.com:felipe0liveira/cars-crud-api.git
cd cars-crud-api
```

### 2. Environment Variables

You will need to configure your environment variables. You can clone `.env.example` file to `.env`

This configuration is focused on the local/dev environment.

### 3. Start the Application

To run the project with **Docker** and **Docker Compose**, use the following command:

```bash
make up

# To see the container logs use:
make logs

# Once you want to turn it off use:
make down

# Alternatively (without Make) you can simply run:
docker-compose up
```

This will build and start the Docker containers.

To force a rebuild of the containers (if you make changes to the `Dockerfile` or dependencies), run:

```bash
make build
```

After the containers are up, you can access the API documentation through:

```
http://localhost:8000/docs
```

## Using the Application

- The API has CRUD endpoints for managing cars (example).
- You can interact with the API via `curl`, `Postman`, or the automatically generated Swagger UI available at `/docs`.

Example endpoints:

- **GET** `/v1/cars`: List all cars.
- **POST** `/v1/cars`: Create a new car.
- **GET** `/v1/cars/{id}`: Get a car by ID.
- **DELETE** `/v1/cars/{id}`: Delete a car by ID.

## Testing the Application

The application contains some integration tests on `tests/`. Feel free to run the tests with the command below:
```bash
make tests
```

## Makefile Commands

The **Makefile** contains several helpful commands to make development easier:

- **`make up`**: Starts the Docker containers (detached).
- **`make build`**: Builds the Docker containers (detached).
- **`make down`**: Stops and removes the Docker containers and volumes.
- **`make clean`**: Cleans up Docker containers, volumes, and images.
- **`make logs`**: Shows logs for the running containers.
- **`make status`**: Shows the status of the Docker containers.
- **`make test`**: Starts running the pytest.
- **`make shell`**: Opens a shell into the `fastapi-app` container.

