#!/bin/bash
# start.sh

# 로그 출력
echo "Starting the FastAPI application with Uvicorn..."

# FastAPI 애플리케이션 시작
uvicorn api:app --host 0.0.0.0 --port 8080
