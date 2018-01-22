all: init test

init:
	python setup.py develop
	pip install tox coverage

test:
	coverage erase
	tox
	coverage html
