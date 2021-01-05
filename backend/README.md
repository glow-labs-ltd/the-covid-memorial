# Local installation and setup

To get the backend up and running:

1. PostgreSQL must be installed and running (see local database setup below).
2. Create and activate a Python virtual environment (see Python commands below).
3. Install python development dependencies (see Python commands below).
4. Run the database migrations (see Python commands below).
5. Run the Python local development server (see Python commands below).

# Commands

## Local database setup

To install postgres:
`brew install postgres`

To run postgres in a docker container locally (docker must be installed and running):
`docker run --rm --name pg-memorial -e POSTGRES_PASSWORD=password -d -p 5432:5432 -v $HOME/docker/volumes/pg-memorial:/var/lib/postgresql/data postgres:13`

Initial set up of postgres database (create the glow database):
`psql -h localhost -U postgres`
`create database glow;`
`\q`

## Python commands

To create a virtual environment:
`virtualenv -p python3 venv` - this will create a venv folder

To active the virtual environment (in venv/ folder):
`source bin/activate`

To install Python development dependencies (in backend/):
`pip install -r requirements-dev.txt`

To run database migrations (in backend/memorial/):
`python manage.py migrate`

To run Python local development server (in backend/memorial/):
`python manage.py runserver`

To create a Django superuser:
`python manage.py createsuperuser`

To run flake8 linting (in backend/memorial/):
`flake8 .`

To run pytest with coverage data (in backend/memorial/):
`pytest --cov=.`
`coverage html` - produce html coverage report
