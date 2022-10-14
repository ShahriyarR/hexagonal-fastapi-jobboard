PYTHON=./.venv/bin/python


install:
	${PYTHON} -m flit install --env --deps=develop

install-dev:
	${PYTHON} -m flit install --env --deps=develop --symlink

format:
	./scripts/format-imports.sh

lint:
	./scripts/lint.sh