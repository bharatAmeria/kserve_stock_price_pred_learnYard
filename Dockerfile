FROM python:3.10-slim

# Optional: Add labels
LABEL maintainer="bharataameriya@gmail.com"
LABEL description="Kubeflow component base image"

# Set workdir
WORKDIR /app

# Copy code
COPY . /app

RUN useradd -m -u 1000 user

# Install Python dependencies
RUN pip install --upgrade pip \
    && pip install -r requirements.txt \
    && rm -rf ~/.cache/pip

RUN chown -R user:user /app

# Set PYTHONPATH so modules can be found
ENV PYTHONPATH=/app

# Optional: Force Python to print stdout/stderr without buffering
ENV PYTHONUNBUFFERED=1

# Optional: Switch to a non-root user (recommended for Kubeflow)

USER user

# Default command can be overridden by Kubeflow component
ENTRYPOINT ["python"]
