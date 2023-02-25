PYTHON=./.venv/bin/python

PHONY = help install install-dev test test-cov run init-db format lint type secure

help:
	@echo "---------------HELP-----------------"
	@echo "To install the project type -> make install"
	@echo "To install the project for development type -> make install-dev"
	@echo "To run application -> make run"
	@echo "To test the project type [exclude slow tests] -> make test"
	@echo "To test the project [only slow tests] -> make test-slow"
	@echo "To test with coverage [all tests] -> make test-cov"
	@echo "To format code type -> make format"
	@echo "To check linter type -> make lint"
	@echo "To run type checker -> make type-check"
	@echo "To run all security related commands -> make secure"
	@echo "------------------------------------"

install:
	${PYTHON} -m flit install --env --deps=develop

install-dev:
	${PYTHON} -m flit install --env --deps=develop --symlink

format:
	${PYTHON} -m isort src tests --force-single-line-imports
	${PYTHON} -m autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place src --exclude=__init__.py
	${PYTHON} -m black src tests --config pyproject.toml
	${PYTHON} -m isort src tests

lint:
	${PYTHON} -m flake8 src
	${PYTHON} -m black src tests --check --diff --config pyproject.toml
	${PYTHON} -m isort src tests --check --diff

run:
	python -m uvicorn src.jobboard.adapters.entrypoints.application:app --host 0.0.0.0 --port 8000 --reload

migrations:
	alembic -c src/jobboard/adapters/db/alembic.ini revision --autogenerate

migrate:
	alembic -c src/jobboard/adapters/db/alembic.ini upgrade head

test:
	TEST_RUN="TRUE" ${PYTHON} -m pytest -svvv -m "not slow" tests

test-slow:
	TEST_RUN="TRUE" ${PYTHON} -m pytest -svvv -m "slow" tests


test-cov:
	TEST_RUN="TRUE" ${PYTHON} -m pytest -svvv --cov-report html --cov=src tests

type:
	${PYTHON} -m pytype --config=pytype.cfg src/*

secure:
	${PYTHON} -m bandit -r src --config pyproject.toml