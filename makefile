test:
	cd ./tests && pytest -v -s

mypy:
	cd ./extr && mypy ./ --ignore-missing-imports
	cd ./tests && mypy ./ --ignore-missing-imports

pylint:
	pylint ./extr

freeze:
	pip freeze > requirements.txt
