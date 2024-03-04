# Use an official lightweight Python image.
FROM python:3.8-slim

# Set the working directory in the container to /app.
WORKDIR /app

# Install Flask
RUN pip install Flask

# Copy the current directory contents into the container at /app.
COPY . /app

# Make port 9090 available to the world outside this container.
EXPOSE 9090

# Run fibonacci_server.py when the container launches.
CMD ["python", "fibonacci_server.py"]
