PYTHON=./.venv/bin/python


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