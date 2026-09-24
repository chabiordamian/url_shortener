# URL Shortener

Small Django REST Framework API for shortening URLs.

The project was kept intentionally simple. It uses SQLite, generates random 8-character codes and stores the mapping between a short code and the original URL.

## Run

Docker with Compose is required.

```sh
docker compose build backend
docker compose run --rm backend python manage.py migrate
docker compose up -d backend
```

The API will be available at:

```text
http://127.0.0.1:8000
```

## API

### Create a short URL

```sh
curl -v http://127.0.0.1:8000/api/urls/ \
  -H 'Content-Type: application/json' \
  -d '{"url":"http://example.com/very-very/long/url/even-longer"}'
```

Example response:

```json
{
  "short_url":"http://127.0.0.1:8000/shrt/PzLplsI9/"
}
```

### Resolve a short URL

```sh
curl http://127.0.0.1:8000/shrt/PzLplsI9/
```

Example response:

```json
{
  "url": "http://example.com/very-very/long/url/even-longer"
}
```

Unknown codes return `404`. Invalid input returns `400`.

## Tests and type checks

```sh
docker compose run --rm backend python manage.py test
docker compose run --rm backend python -m mypy
```

## Notes

* Only HTTP and HTTPS URLs are accepted.
* Original URLs can be up to 2048 characters.
* Short codes contain eight random letters and digits.
* `short_code` has a unique constraint in the database.
* If a generated code already exists, another code is generated. Creation is retried up to three times.
* Shortening the same URL multiple times creates separate short codes.
* Resolving a short URL returns JSON instead of performing an HTTP redirect.
* SQLite is used to keep the project easy to run locally.

This is a development setup using Django's development server and debug configuration.
