# Docker Setup for Open License Media Search Application

This guide will help you set up and run the application using Docker.

## Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed on your machine
- Git repository cloned to your local machine

## Steps to Run with Docker

1. Open a terminal or command prompt in the project directory

2. Build and start the Docker containers:
   ```
   docker-compose up --build
   ```
   This command will:
   - Build the Docker image
   - Start the container
   - Initialize the database
   - Run the application

3. Access the application:
   - Open your browser and go to http://localhost:5000

4. To stop the container:
   ```
   docker-compose down
   ```

## Development with Docker and Cursor Editor

1. Install Cursor Editor from https://cursor.sh/

2. Open the project folder in Cursor Editor:
   - Launch Cursor
   - Select "Open Folder" and navigate to your project directory

3. While Docker is running, make changes to your code using Cursor Editor

4. The changes will be reflected in the Docker container because of the volume mapping in docker-compose.yml:
   ```yaml
   volumes:
     - ./app:/app/app
     - ./migrations:/app/migrations
   ```
   This maps your local app folder to the app folder in the container

5. If you make changes to requirements.txt or Dockerfile, you'll need to rebuild:
   ```
   docker-compose down
   docker-compose up --build
   ```

## Docker Commands Reference

- Build and start containers: `docker-compose up --build`
- Start containers in detached mode: `docker-compose up -d`
- Stop containers: `docker-compose down`
- View logs: `docker-compose logs -f`
- Shell access to container: `docker exec -it open-license-media bash`
- List running containers: `docker ps`
- Remove all containers and volumes: `docker-compose down -v`

## Troubleshooting

- If the application fails to start, check the logs using `docker-compose logs -f`
- If database issues occur, try removing the volume with `docker-compose down -v` and then rebuilding
- Make sure ports are not in use by other applications 