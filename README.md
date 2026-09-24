# URL shortener

A small Django REST Framework API for shortening URLs and retrieving the original address.

## Run

Requires Docker with Compose. From the project directory:

```sh
docker compose build backend
docker compose run --rm backend python manage.py migrate
docker compose up -d backend
```

## API

Create a short URL:

```sh
curl -X POST http://localhost:8000/api/urls/ \
  -H 'Content-Type: application/json' \
  -d '{"url":"http://example.com/very-very/long/url/even-longer"}'
```

Returns HTTP 201 with `{"short_url":"http://localhost:8000/shrt/<code>/"}`.
Use the returned address to retrieve the original URL:

```sh
curl 'http://localhost:8000/shrt/<code>/'
```

Returns HTTP 200 with `{"url":"http://example.com/very-very/long/url/even-longer"}`.
Invalid input returns 400; an unknown code returns 404.

## Checks

```sh
docker compose run --rm backend python manage.py test
docker compose run --rm backend python -m mypy
```

## Assumptions

- HTTP and HTTPS URLs only, up to 2048 characters. Resolving returns JSON, not a redirect.
- Shortening the same URL again creates a separate code. Target pages are not fetched.
- Codes contain eight random letters and digits. The database enforces uniqueness; a collision currently returns 500. Retries are omitted to keep the exercise small.
- SQLite data lives in `db.sqlite3` in the mounted project directory and survives container recreation.
- This is a local development setup: debug mode, Django's development server and a development secret key. Optionally set `DJANGO_SECRET_KEY` in your shell or a local `.env` file; Compose passes it to Django. These files are ignored by Git and Docker.
