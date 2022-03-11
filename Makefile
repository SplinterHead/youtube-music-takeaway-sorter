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
	MUSIC_ROOT="/music/root" poetry run pytest -vv -s

.PHONY: check
check: format test

.PHONY: run
run:
	poetry run python yt-sorter.py
