PYTHON := python3
NAME := a_maze_ing.py
CONFIG := config.txt

run:
	$(PYTHON) $(NAME) $(CONFIG)

install:
	@echo "This Project needs no external dependencies!"
	@echo "Nothing to be installed..."

debug:
	$(PYTHON) -m pdb $(NAME) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf output_maze.txt

lint:
	flake8 .; mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .; mypy . --strict

.PHONY: install run debug clean lint lint-strict
