FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set up working directory
WORKDIR /workspace

# Install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Configure Git to avoid dubious ownership and set default identity
RUN git config --global --add safe.directory /workspace && \
    git config --global user.email "mlops-agent@example.com" && \
    git config --global user.name "MLOps Agent"

# The command will be overridden in docker-compose for the long running app service,
# or executed directly when running single commands.
CMD ["tail", "-f", "/dev/null"]
