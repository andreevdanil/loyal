# Backend part of Loyal app (in progress)

## Introduction
It is study project for course at HSE University. So, is not a production ready solution.

Loyal is a product which aggregate loyalty programs from different businesses.

## Requirements
* [Python 3.9](https://www.python.org)
* [Poetry 1.1](https://python-poetry.org)
* [Make](https://www.gnu.org/software/make/)
* [Docker 19](https://docs.docker.com/)
* [Docker Compose](https://docs.docker.com/compose/) (optional)

## Installation
To create [virtual environment](https://docs.python.org/3.8/library/venv.html) and install all dependencies run:

```bash
make setup
```

If you want to update dependency versions you must run:

```bash
make update
```

## Run
To run a production server (via [gunicorn](https://gunicorn.org/)):

```bash
gunicorn main:create_app -c gunicorn.config.py
```

Use virtual environment variables to configure the application to run.

## Deploy
Application is ready to deploy to [Heroku](https://heroku.com).

All that you need is run:
```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
```
Then you can deploy it to Heroku.

### Environment variables
| Variable                                | Required | Default                         |
|-----------------------------------------|----------|---------------------------------|
| DATABASE_URL                            | Yes      |                                 |
| DATABASE_POOL_MIN_SIZE                  | No       | 1                               |
| DATABASE_POOL_MAX_SIZE                  | No       | 5                               |

## Docker
It is recommend using prepared scripts to work with Docker.

To build a new image, run the command:

```bash
make build
```

As a result, you will get a new image `loyal:latest`.

### Docker Compose
In the `examples` folder you can find `docker-compose.yml` file with ready description of required containers.

## Tests
`Not ready yet`

## Checking
Use linters to check the written code:

[pylint](https://www.pylint.org/) (static code analysis tool):

```bash
make pylint
```

[mypy](http://mypy-lang.org/) (static type checker):

```bash
make mypy
```

[flake8](http://flake8.pycqa.org/en/latest/) (style guide enforcement tool):

```bash
make flake
```

And formatters:

[isort](https://github.com/timothycrosley/isort) (utility to sort imports):

```bash
make isort
```

[add-trailing-comma](https://github.com/asottile/add-trailing-comma) 
(utility to automatically add trailing commas to calls and literals):

```bash
make trailing
```

To run all commands use the shortcut:

```bash
make format lint
```
