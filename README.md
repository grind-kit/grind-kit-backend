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

- Run `docker-compose exec app python manage.py test` while the container is running to run all tests
- To run a specific test, run `docker-compose exec app python manage.py test <app>.<test_file>.<test_class>.<test_function>`

## Contributing

- Create a new branch off of `development` with the name of the feature you're working on
- Naming convention: `feat/<feature_name>`, `fix/<fix_name>`, `refactor/<refactor_name>`
- For example, if you're working on fixing the login page, your branch name would be `fix/login-page`
- For your commits, please follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification
- If you're working on a feature that requires a new model, or a change to an existing model, please create a migration file for it
- When you're done with your feature branch, create a pull request from your branch to `development`
- In the pull request description, please include what you added/changed, and any other relevant information
- Once your pull request is approved, it will be merged into `development`

## URLs

- Local: http://localhost:8000
- Admin: http://localhost:8000/admin
