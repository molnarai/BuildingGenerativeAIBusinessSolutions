FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY run.sh .

# Create data directories
RUN mkdir -p /data/input /data/output

# Make run script executable
RUN chmod +x run.sh

CMD ["./run.sh"]