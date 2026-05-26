# BugTrack Django Ticketing App

A compact Django ticketing app for creating and managing tickets, users, and assignments.

## Overview

This project is a simple issue tracker built with Django. It includes user authentication, ticket CRUD operations, ticket assignment, and user profile views.

## Core features

- User signup, login, and logout
- Custom user model with display name, homepage, and age
- Ticket creation, detail view, edit, and delete
- Assignment of tickets to active users
- Status tracking for New, In Progress, Done, and Invalid
- User profile pages showing assigned and created tickets
- SQLite by default, with optional production database configuration via `DATABASE_URL`

## Project structure

- `myticket/` — Django project configuration, URL routing, settings, and WSGI setup
- `tickets/` — main app with models, views, forms, and business logic
- `templates/` — HTML templates for pages and layouts
- `static/` — CSS, JavaScript, and theme assets
- `db.sqlite3` — default local database

## Requirements

- Python 3.13
- Django 6.x
- Whitenoise
- dj-database-url
- psycopg2-binary
- Gunicorn (for production deployment)

## Setup

1. Create and activate a Python virtual environment:

```bash
cd my_django_project
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Apply database migrations:

```bash
python manage.py migrate
```

4. Create a superuser (optional):

```bash
python manage.py createsuperuser
```

5. Run the development server:

```bash
python manage.py runserver
```

6. Visit the application:

```text
http://127.0.0.1:8000/
```

## Environment variables

The app supports the following optional environment variables:

- `SECRET_KEY` — Django secret key
- `DEBUG` — `True` or `False`
- `ALLOWED_HOSTS` — comma-separated hostnames
- `DATABASE_URL` — production database connection string
- `CSRF_TRUSTED_ORIGINS` — comma-separated trusted origins

## Authentication and authorization

- Uses the custom user model `tickets.MyUser`
- Signup captures `username`, `password`, `display_name`, and `age`
- Logged-in users can create tickets and view profiles
- Only the ticket creator or staff users may edit or delete tickets

## Deployment notes

- Static files are served with WhiteNoise
- Use Gunicorn for production WSGI hosting
- Set `DEBUG=False` in production
- Configure `ALLOWED_HOSTS` and use `DATABASE_URL` for PostgreSQL or other external databases

## Useful commands

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
python manage.py createsuperuser
```

## Testing

- Run the Django test suite:

```bash
python manage.py test
```

- If you add tests, keep them small and focused on one behavior at a time.

## Notes

- Templates are located in the `templates/` directory
- The ticket app is implemented in `tickets/`
- Default local database file is `db.sqlite3`

## Contributing

Contributions are welcome. For improvements or bug fixes:

- Fork the repository
- Create a new branch for your feature or fix
- Run tests locally before submitting a pull request
- Keep changes focused and add comments for any custom logic

## Known limitations

- No email notifications are implemented for ticket updates
- Ticket permissions are simple: only creators and staff can edit/delete
- There is no pagination or search on the ticket list view
- User profiles do not support editing from the frontend at this time

