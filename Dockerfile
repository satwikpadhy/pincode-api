# Use official Python image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source code
COPY . .

# Expose port (adjust if needed)
EXPOSE 6901

# Set environment variable for Uvicorn host and port (optional)
ENV HOST=0.0.0.0
ENV PORT=6901

# Command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "6901", "--log-level", "error"]
