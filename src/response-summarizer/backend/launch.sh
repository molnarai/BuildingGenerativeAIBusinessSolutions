#!/bin/bash
docker build -t response-summarizer-backend .
docker run --rm -d \
    --name response-summarizer \
    -p 5005:5000 \
    -v response-data:/app/data \
    --add-host=host.docker.internal:host-gateway \
    response-summarizer-backend