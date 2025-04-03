
deps:
	pip install -r requirements.txt

deps-dev:
	pip install -r requirements.dev.txt

format:
	isort .
	black .

check:
	mypy --implicit-optional .