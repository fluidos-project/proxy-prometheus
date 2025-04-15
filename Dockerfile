FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy proxy code
COPY proxy_prometheus.py .

# Expose the port
EXPOSE 8080

# Set env path and run
ENV PYTHONUNBUFFERED=1
CMD ["python", "proxy_prometheus.py"]
