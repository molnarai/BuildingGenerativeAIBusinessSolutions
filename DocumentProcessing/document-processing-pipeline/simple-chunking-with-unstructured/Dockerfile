FROM downloads.unstructured.io/unstructured-io/unstructured:latest
USER root
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/
COPY run.sh .

# Create data directories
RUN mkdir -p /data/input /data/output

# # Make run script executable
RUN chmod a+x run.sh

CMD ["./run.sh"]