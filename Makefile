PROJECT := loyal

VENV := .venv
export PATH := $(VENV)/bin:$(PATH)

REPORTS := .reports
COVERAGE := $(REPORTS)/coverage

SOURCES := $(PROJECT) gunicorn.config.py main.py
MIGRATIONS := migrations

PY_FILES = $(shell find $(SOURCES) -name "*.py")

IMAGE_NAME := $(PROJECT)

clean:
	rm -rf .mypy_cache
	rm -rf $(REPORTS)
	rm -rf $(VENV)

$(VENV):
	poetry install --no-root --extras pytest-plugin

$(REPORTS):
	mkdir $(REPORTS)

setup: $(VENV) $(REPORTS)

update: setup
	poetry update

mypy: setup
	mypy $(SOURCES) $(MIGRATIONS)

pylint: setup
	pylint $(SOURCES) $(MIGRATIONS) > $(REPORTS)/pylint.txt

flake: setup
	flake8 $(SOURCES) $(MIGRATIONS)

bandit: setup
	bandit -q -f json -o $(REPORTS)/bandit.json -r $(SOURCES) $(MIGRATIONS) -s B101

isort: setup
	isort -rc $(SOURCES)

isort-lint: setup
	isort -c -rc $(SOURCES)

trailing: setup
	@add-trailing-comma $(PY_FILES) --py36-plus --exit-zero-even-if-changed

trailing-lint: setup
	@add-trailing-comma $(PY_FILES) --py36-plus

lint: isort-lint trailing-lint mypy pylint flake bandit

format: isort trailing

build: lint
	DOCKER_BUILDKIT=1 docker build --ssh default=$(SSH_KEY_PATH) . -t $(IMAGE_NAME) --pull

all: format lint build

.DEFAULT_GOAL := all
