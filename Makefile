# Usage:
# make run

.DEFAULT_GOAL := run

.venv: .venv/touchfile

.venv/touchfile: requirements.txt
	test -d .venv || python -m venv .venv
	. .venv/bin/activate; pip install -Ur requirements.txt; pip install -Ur requirements-test.txt
	touch .venv/touchfile

precommit: .venv
	. .venv/bin/activate
	pre-commit run --all-files

clean:
	rm -rf .venv

dump:
	./myphotos.sh

run:
	python myphotos.py

all: precommit dump run
