# Use an official lightweight Python image.
FROM python:3.8-slim

# Set the working directory in the container to /app.
WORKDIR /app

# Install Flask and Requests
RUN pip install Flask requests

# Copy the current directory contents into the container at /app.
COPY . /app

# Make port 8080 available to the world outside this container.
EXPOSE 8080

# Define the command to run the Flask application.
CMD ["python", "user_server.py"]
