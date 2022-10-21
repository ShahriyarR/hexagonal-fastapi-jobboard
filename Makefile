PYTHON=./.venv/bin/python

PHONY = help install install-dev test test-cov run init-db format lint

help:
	@echo "---------------HELP-----------------"
	@echo "To install the project type -> make install"
	@echo "To install the project for development type -> make install-dev"
	@echo "To test the project type -> make test"
	@echo "To test with coverage html type -> make test-cov"
	@echo "To run the project type -> make run"
	@echo "To format code type -> make format"
	@echo "To check linter type -> make lint"
	@echo "------------------------------------"

install:
	${PYTHON} -m flit install --env --deps=develop

install-dev:
	${PYTHON} -m flit install --env --deps=develop --symlink

format:
	./scripts/format-imports.sh

lint:
	./scripts/lint.sh

run:
	python -m uvicorn src.jobboard.adapters.entrypoints.application:app --reload

migrations:
	alembic -c src/jobboard/adapters/db/alembic.ini revision --autogenerate

migrate:
	alembic -c src/jobboard/adapters/db/alembic.ini upgrade head

test:
	${PYTHON} -m pytest -svv tests

test-cov:
	${PYTHON} -m pytest --cov-report html --cov=src tests