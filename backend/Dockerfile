FROM python:3.9-alpine

# Install R
RUN apt-get update && apt-get install -y \
    r-base \
    r-base-dev \
    && rm -rf /var/lib/apt/lists/*

# Install R packages
RUN R -e "install.packages(c('ggplot2', 'plotly', 'rgl'), repos='http://cran.rstudio.com/')"

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
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]