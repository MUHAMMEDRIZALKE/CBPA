#!/bin/bash

uv run alembic upgrade head
uv run app/main.py