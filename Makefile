SHELL := /bin/bash

# --- Load .env into Make (works if lines are KEY=VAL) ---
ifneq (,$(wildcard .env))
include .env
# Export all keys defined in .env into the environment of each recipe
export $(shell sed -n 's/^\([A-Za-z_][A-Za-z0-9_]*\)=.*/\1/p' .env)
endif

POETRY      = poetry
PYTHON      = $(POETRY) run python
ALEMBIC     = $(POETRY) run alembic
API_DIR 	= apps/api
UI_DIR      = apps/admin-ui

run-api: ## Run FastAPI dev server
	cd $(API_DIR) && $(POETRY) run uvicorn app.main:app --reload --port 8000
