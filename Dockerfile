FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    dos2unix \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p uploads data logs chroma_db

# Fix line endings for Linux and make executable
RUN dos2unix start.sh && chmod +x start.sh

# Expose both ports (API + Streamlit)
EXPOSE 8000 8501

CMD ["./start.sh"]
