PYTHON := python3
NAME := a-maze-ing.py

install:
	@echo "This Project needs no external dependencies!"
	@echo "Nothing to be installed..."

run:
	$(PYTHON) $(NAME)

debug:
	$(PYTHON) -m pdb $(NAME)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .mypy_cache
	rm -rf output_maze.txt

lint:
	flake8 .; mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

lint-strict:
	flake8 .; mypy . --strict

.PHONY: install run debug clean lint lint-strict
