#!/bin/bash

echo " Running tests with coverage..."

PYTHONPATH=src pytest tests/ --cov=multi_repo_analyzer --cov-report=term-missing --disable-warnings -v
