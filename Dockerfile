# Dockerfile for Fakturownia / InvoiceOcean MCP (Background Service)
FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy dependency files
COPY requirements.txt .
COPY pyproject.toml .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the source code
COPY main.py .

# The MCP server will run over stdio, but when used as a background service 
# it can also be started as a persistent process.
ENTRYPOINT ["python", "main.py"]
