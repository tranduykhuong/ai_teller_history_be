# OpenVNU BE

## File structure

```
.
├── api
│   ├── apps.py
│   ├── exceptions.py
│   ├── firebase.py
│   ├── mail.py
│   ├── mixins.py
│   ├── permissions.py
│   ├── routes.py
│   ├── tests.py
│   ├── urls.py
│   ├── utils.py
│   └── views.py
├── authentication
│   ├── migrations
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   └── views
├── openVNU
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates
│   └── email
├── manage.py
├── README.md
├── Dockerfile
├── requirements.txt
└── ...
```

## Table of Contents

- [Tech Stack](#techstack)
- [Features](#features)
- [Environment Variables](#environment-variables)
- [Run Locally](#run-)
- [Development](#development)
- [Running tests](#running-tests)
- [Acknowledgements](#acknowledgements)
- [License](#license)

## Tech Stack

- Django
- REST-framework
- JWT (Authentication)
- PostgreSQL (Database)
- Firebase store

## Features

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

## Run Locally

Clone the project

```bash
  git clone ...
```

Go to the project directory

Install dependencies

```bash
  pip install -r requirements.txt
```

Migration

```bash
  python manage.py migrate
```

Start the server

```bash
  python manage.py runserver
```

## Development

To run program in product environment:

- docker and docker-compose
- git

1. Clone the reposity:

```bash
    git clone ...
```

2. From within the repository directory, run:

```bash
    docker-compose up --build
```

## Branching Strategy:

1. **Develop Branch (Staging):**
   - The `develop` branch is designated for staging deployments.
   - All feature branches should be merged into `develop` for testing and staging purposes.
   - Developers are encouraged to create feature branches from `develop`.

2. **Main Branch (Production):**
   - The `main` branch is reserved for production deployments.
   - Only thoroughly tested and approved changes from the `develop` branch should be merged into `main`.
   - It is crucial to ensure that only stable and production-ready code is pushed to the `main` branch.

## Deployment Process:

### Staging Deployment:

### Production Deployment:

1. **Merge to Main:**
   - Only approved changes from the `develop` branch should be merged into the `main` branch for production.

2. **Monitoring:**
   - Monitor the production environment closely for any unexpected issues.
   - Rollback procedures should be in place in case of critical problems.

3. **Communication:**
   - Communicate the successful production deployment to the team and stakeholders.

*By following these guidelines, you establish a clear separation between staging and production environments, ensuring that only thoroughly tested and approved changes are deployed to production.*

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [REST Framework](https://www.django-rest-framework.org/)
- [JWT Authentication](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/)
- [Docker](https://www.docker.com/)

## Running Tests

To run tests, run the following command

```bash
  python manage.py test
```

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Support

For support, email tranduykhuongit@gmail.com for supports.
