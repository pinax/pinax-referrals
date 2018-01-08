all: init test

init:
	python setup.py develop
	pip install tox coverage Sphinx

test:
	coverage erase
	tox
	coverage html
