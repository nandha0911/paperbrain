FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create necessary directories
RUN mkdir -p uploads data logs chroma_db

# Expose both ports (API + Streamlit)
EXPOSE 8000 8501

# Start script: run both backend API and Streamlit frontend
COPY start.sh .
RUN chmod +x start.sh
CMD ["./start.sh"]
