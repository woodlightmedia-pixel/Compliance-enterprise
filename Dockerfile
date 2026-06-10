# =====================================================================
# Step 1: Use an official, lightweight Python base image
# =====================================================================
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files to disk and force unbuffered logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory inside the container
WORKDIR /app

# =====================================================================
# Step 2: Install system dependencies & compile components
# =====================================================================
# slim images don't have build tools; we install curl for healthchecks if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# =====================================================================
# Step 3: Layer caching for Python dependencies
# =====================================================================
# Copy only requirements first to leverage Docker's layer caching
COPY requirements.txt .

# Install dependencies directly into the system space (no venv needed inside containers)
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# =====================================================================
# Step 4: Copy application directories and assets
# =====================================================================
# Copy your private application source code and knowledge templates
COPY src/ ./src/
COPY knowledge_base/ ./knowledge_base/
COPY .well-known/ ./.well-known/

# Expose port 8000 for your main FastAPI router engine
EXPOSE 8000

# =====================================================================
# Step 5: Enforce Non-Root Security Best Practices
# =====================================================================
# Create a dedicated, unprivileged system user so the container doesn't run as root
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser

# =====================================================================
# Step 6: Define Execution Command
# =====================================================================
# Run uvicorn server in production mode to drive your sequential ADK pipeline
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]