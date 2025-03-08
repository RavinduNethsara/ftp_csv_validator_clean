# Use official Python image as base
FROM python:3.12

# Set working directory inside the container
WORKDIR /app

# Copy all project files into the container
COPY . /app

# Install required dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the main application
CMD ["python", "main.py"]
