# syntax=docker/dockerfile:1.0-experimental

FROM python:3.8-buster as builder

COPY . .

RUN pip install -U --no-cache-dir pip wheel setuptools poetry

RUN poetry build -f wheel
RUN poetry export -f requirements.txt -o requirements.txt --without-hashes

RUN pip wheel -w dist -r requirements.txt


FROM python:3.8-slim-buster as runtime

WORKDIR /usr/src/app

ENV PYTHONOPTIMIZE=1

COPY --from=builder dist dist
COPY --from=builder migrations migrations
COPY --from=builder alembic.ini gunicorn.config.py main.py ./

RUN pip install --no-cache-dir --no-index dist/*.whl

RUN useradd -r -UM app
USER app

CMD ["gunicorn", "main:create_app", "-c", "gunicorn.config.py"]
