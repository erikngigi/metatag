# Variables
APP_ENTRY := -m metatag.main

.PHONY: all help list install-python sync clear run run-preview test build clean run-dry

all: sync clean build

help: ## Prints help for targets with comments
	@cat $(MAKEFILE_LIST) | grep -E '^[a-zA-Z_-]+:.*?## .*$$' | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

list: ## View available and installed Python versions
	uv python list

install-python: ## Install a specific python version (usage: make install-python VERSION=3.13)
	uv run install 3.14

sync: ## Sync dependencies and set up the virtual environment
	uv sync

clear: ## Clear terminal screen
	clear

run: clear ## Run the interactive CLI application
	uv run python $(APP_ENTRY) --interactive

run-preview: clear ## Run the interactive CLI application in preview mode (--interactive --preview)
	uv run python $(APP_ENTRY) --interactive --preview

test: ## Run tests (placeholder)
	@echo "No test configured yet"

build: ## Build standalone binary executable using PyInstaller
	uv run pyinstaller --onefile --name metatag metatag/main.py
	ln -sf $(shell pwd)/dist/metatag ~/.local/bin/metatag

clean: ## Remove build artifacts, cache files, and dist folders
	rm -rf dist/ build/ *.egg-info .pytest_cache .uv_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
