.PHONY: install
install:
	poetry update
	poetry install

.PHONY: format
format:
	poetry run black .
	poetry run isort --profile black .

.PHONY: test
test:
	poetry run pytest -vv -s

.PHONY: run
run:
	poetry run python yt-sorter.py
