# Use a lightweight Python image
FROM python:3.10-slim

# Set work directory inside container
WORKDIR /app

# Install system dependencies if needed (add more if your src requires)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only required files into the image
COPY src/ /app/src/
COPY setup.py /app/
COPY project.toml /app/
COPY config.yaml /app/
COPY .env /app/
COPY requirements.txt /app/
COPY .project-root /app/
COPY kubeflow/* /app/kubeflow/

# Install dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && pip install -e .


# Create runtime folders (so pipeline won’t error out if missing)
RUN mkdir -p /app/artifacts /app/logs

# Set environment variables (optional)
ENV PYTHONPATH=/app

# Default command (can be overridden in pipeline spec)
CMD ["python", "-m", "src.main"]
