#!/bin/bash
alembic -c ./alembic.ini upgrade head --sql
uvicorn main:app --host 0.0.0.0 --port 8000
