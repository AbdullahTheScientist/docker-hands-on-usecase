# FROM python:3.9-slim

# # Install system dependencies including wkhtmltopdf
# RUN apt-get update && apt-get install -y \
#     wkhtmltopdf \
#     xvfb \
#     && rm -rf /var/lib/apt/lists/*

# # Set working directory
# WORKDIR /app

# # Copy requirements first for better caching
# COPY requirements.txt .

# # Install Python dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Copy application code
# COPY . .

# # Create directories
# RUN mkdir -p templates generated_resumes

# # Expose port
# EXPOSE 8000

# # Create startup script
# RUN echo '#!/bin/bash\nPORT=${PORT:-8000}\nexec gunicorn app:app -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT' > /start.sh
# RUN chmod +x /start.sh

# # Run the application
# CMD ["/start.sh"]














FROM python:3.9-slim

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Update package list and install basic dependencies first
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    software-properties-common \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install wkhtmltopdf and basic tools
RUN apt-get update && apt-get install -y \
    wkhtmltopdf \
    xvfb \
    fontconfig \
    && rm -rf /var/lib/apt/lists/*

# Install available fonts (removing problematic ones)
RUN apt-get update && apt-get install -y \
    fonts-dejavu-core \
    fonts-dejavu-extra \
    fonts-liberation \
    fonts-noto-core \
    fonts-freefont-ttf \
    && rm -rf /var/lib/apt/lists/*

# Try to install Microsoft fonts (optional - will continue if it fails)
RUN apt-get update && \
    (echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections && \
    apt-get install -y --no-install-recommends ttf-mscorefonts-installer || echo "Microsoft fonts installation failed, continuing...") && \
    rm -rf /var/lib/apt/lists/*

# Update font cache
RUN fc-cache -fv || echo "Font cache update failed, continuing..."

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

# Create startup script with font environment variables
RUN echo '#!/bin/bash\n\
export FONTCONFIG_PATH=/etc/fonts\n\
export FONTCONFIG_FILE=/etc/fonts/fonts.conf\n\
PORT=${PORT:-8000}\n\
exec gunicorn app:app -w 2 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:$PORT' > /start.sh

RUN chmod +x /start.sh

# Run the application
CMD ["/start.sh"]