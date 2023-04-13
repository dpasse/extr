test:
	cd ./tests && pytest -v -s

mypy:
	cd ./src/extr && mypy ./ --ignore-missing-imports
	cd ./tests && mypy ./ --ignore-missing-imports

pylint:
	pylint ./src/extr

freeze:
	pip freeze > requirements.txt

build:
	python setup.py sdist
	python setup.py bdist_wheel

clean-build-win:
	rmdir /S .\build
	rmdir /S .\dist
	rmdir /S .\src\extr.egg-info
