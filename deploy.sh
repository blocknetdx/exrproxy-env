#!/bin/bash
docker-compose pull
docker-compose --env-file .env -f "docker-compose.yml" up -d --build