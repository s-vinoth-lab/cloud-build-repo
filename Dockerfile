# Use an official Python runtime as a parent image
FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt ./

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY app.py .

# Expose the port that the Flask app will run on
EXPOSE 8080

# Run the application using Gunicorn
# Gunicorn will listen on all interfaces (0.0.0.0) and on port 8080
# It will use a single worker process for simplicity, but in production, you might want more
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
