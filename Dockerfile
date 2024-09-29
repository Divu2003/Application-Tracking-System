# Use a Python base image
FROM python:3.11-slim

# Install Poppler
RUN apt-get update && apt-get install -y poppler-utils && apt-get clean

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Expose the desired port (adjust if necessary)
EXPOSE 8000

# Command to run the application
CMD ["python", "app.py"]  # Change app.py to your entry file
