FROM python:3.9-slim

# Install R and required packages
RUN apt-get update && apt-get install -y \
    r-base \
    r-base-dev \
    libcurl4-openssl-dev \
    libssl-dev \
    libxml2-dev \
    libglu1-mesa-dev \
    libgl1-mesa-dev \
    libpng-dev \
    libcairo2-dev \
    libxt-dev \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install xvfb for headless rendering
RUN echo '#!/bin/bash\nxvfb-run -a "$@"' > /usr/local/bin/xvfb-run-safe \
    && chmod +x /usr/local/bin/xvfb-run-safe

# Install R packages with additional error handling
RUN xvfb-run-safe R -e "options(warn=2); \
    install.packages('ggplot2', repos='http://cran.rstudio.com/', dependencies=TRUE); \
    install.packages('htmlwidgets', repos='http://cran.rstudio.com/', dependencies=TRUE); \
    install.packages('plotly', repos='http://cran.rstudio.com/', dependencies=TRUE); \
    install.packages('rgl', repos='http://cran.rstudio.com/', dependencies=TRUE);"

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY . .

# Create temp directory
RUN mkdir -p temp

# Expose port
EXPOSE 5001

# Run the application
CMD ["python", "app.py"]