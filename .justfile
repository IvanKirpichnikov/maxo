lint:
    ruff check 
    mypy
    codespell src examples
    bandit src -r
    slotscheck src

format:
    ruff format
