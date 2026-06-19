# Stage 1: Build the React frontend
FROM node:22-alpine AS frontend-build

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ .
RUN npm run build

# Stage 2: Python backend with built frontend
FROM python:3.12-slim

WORKDIR /app

# Copy backend
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

# Copy built frontend
COPY --from=frontend-build /app/frontend/dist /app/static

# Expose the public port
EXPOSE 3000

# Run the server bound to all interfaces on port 3000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]