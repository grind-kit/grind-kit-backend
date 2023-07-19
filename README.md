# Grind Kit - Backend

## Technologies
- Python
- Django
- PostgreSQL

## Setup

1. Install Docker on your machine
2. Clone this repository to your machine
3. Copy the `.env.local.example` file to a new file called `.env` at the root of the project, and fill in the values
4. Run `docker-compose build` to build the Docker image
5. Run `docker-compose up` to start the Docker container

- If you want to run the container in daemon mode, run `docker-compose up -d`
- If you need to rebuild the container, run `docker-compose up --build`
- If you need to stop the container, run `docker-compose stop`

6. To migrate the database, run `docker-compose exec app python manage.py migrate` while the container is running

## Running Tests

Run `docker-compose exec app python manage.py test` while the container is running

## URLs

- Local: http://localhost:8000
- Admin: http://localhost:8000/admin