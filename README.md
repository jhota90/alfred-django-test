# Django Bank API

This project is a Django REST Framework API to manage `Address`, `Driver`, and `Service` entities. Allows users to create, retrieve, update, and delete records.

## Technologies

- Django
- Django REST Framework
- PostgreSQL (or other database of your choice)
- Docker

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/)

### Clone the Repository

```bash
git clone https://github.com/jhota90/alfred-django-test.git
cd alfred-django-test
```

#### Build the Docker images
```bash
docker-compose build
```

#### Run the application
```bash
docker-compose up -d
```

#### Running Django Tests
```bash
docker-compose run app python manage.py test
```

#### Running PyTests
```bash
docker-compose run app pytest
```

#### Stop the application
```bash
docker-compose down
```