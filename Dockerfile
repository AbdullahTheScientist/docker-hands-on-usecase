FROM python:3.9-slim

# Install system dependencies including wkhtmltopdf
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create directories
RUN mkdir -p templates generated_resumes

# Expose port
EXPOSE 8000

# Create startup script
RUN echo '#!/bin/bash\nPORT=${PORT:-8000}\nexec gunicorn app:app -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT' > /start.sh
RUN chmod +x /start.sh

# Run the application
CMD ["/start.sh"]