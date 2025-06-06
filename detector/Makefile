SHELL := /bin/bash

.PHONY: help dev mock-pdf
.DEFAULT: help

help:
	@echo "make dev"
	@echo "          Run agent in dev env"
	@echo "----------"
	@echo "make mock-pdf"
	@echo "          Generate PDF file with mocked data"
	@echo "----------"

dev:
	@echo "Running agent in local env ..."
	@echo "----------"
	uv run src/__main__.py

mock-pdf:
	@echo "Generating PDF file with mocked data ..."
	@echo "----------"
	uv run data/src/__init__.py