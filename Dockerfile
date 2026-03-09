# Use Python 3.10 slim image as base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies (if needed for Poetry or other tools)
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Set work directory
WORKDIR /app

# Copy dependency files
COPY pyproject.toml poetry.lock* README.md ./
COPY sample_data ./sample_data

# Configure Poetry: don't create virtual environment since we're in container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-root

# Copy project code
COPY . .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port if running API (optional, since CLI is main)
# EXPOSE 8000

# Default command: run the CLI
CMD ["python", "-m", "laika_pipeline"]