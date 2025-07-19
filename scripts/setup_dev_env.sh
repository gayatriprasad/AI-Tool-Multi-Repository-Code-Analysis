#!/bin/bash

echo " Setting up development environment..."

# Install with all extras (AI + dev)
pip install -e .[all]

# Optional: install pre-commit hooks
if [ -f .pre-commit-config.yaml ]; then
  echo " Installing pre-commit hooks..."
  pre-commit install
fi

echo " Environment setup complete."
