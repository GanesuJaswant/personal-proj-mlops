# Lab 11: Containerization & Image Optimization Report

## 1. Overview
The Car Price Prediction inference API was containerized using a multi-stage Docker build strategy based on `python:3.11-slim`.

## 2. Multi-Stage Optimization
- **Builder Stage**: Compiles and installs Python wheels into `/root/.local`.
- **Production Stage**: Copies only installed packages and application source files to minimize image footprint.
- **Security**: The service runs under an unprivileged user (`appuser`, UID 1000).

## 3. Container Specifications
- **Base Image**: `python:3.11-slim`
- **Exposed Port**: `8000`
- **Healthcheck**: `GET /health` polled every 30s
- **Resource Constraints**: 250m CPU, 256Mi RAM minimum request.
