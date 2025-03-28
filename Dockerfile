# Use the official Python image as the base image
FROM python:3.12-slim

# Set the working directory
WORKDIR /app

# Copy the requirements file into the container
COPY backend/requirements.txt .

# Install the required Python packages
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

RUN ls -la /app

# Expose the port that your Flask app listens on
EXPOSE 5000

# Start the Flask app
CMD ["python", "backend/src/app.py"]