# ziip

Django 6.0 web application

## Project Structure

```
ziip/
├── ziip/               # Django project settings
│   ├── settings.py     # Project configuration
│   ├── urls.py         # URL routing
│   ├── wsgi.py         # WSGI configuration
│   └── asgi.py         # ASGI configuration
├── comments/           # Comments app
│   ├── models.py       # Data models
│   ├── views.py        # View logic
│   ├── admin.py        # Admin configuration
│   └── migrations/     # Database migrations
├── templates/          # HTML templates
├── manage.py           # Django management commands
└── pyproject.toml      # Project dependencies
```

## Tech Stack

- Python 3.14
- Django 6.0
- Django REST Framework 3.16.1
- SQLite (development database)

## Development Tools

- Black (code formatter)
- Ruff (linter)
- Pytest (testing framework)

## Getting Started

```bash
# Install dependencies
uv sync

# Run development server
python manage.py runserver

# Apply migrations
python manage.py migrate
```
