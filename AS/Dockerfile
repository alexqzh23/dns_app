# Use an official lightweight Python image.
FROM python:3.8-slim

# Set the working directory in the container to /app.
WORKDIR /app

# Copy the current directory contents into the container at /app.
COPY . /app

# Make port 53533 available to the world outside this container.
EXPOSE 53533/udp

# Run authoritative_server.py when the container launches.
CMD ["python", "authoritative_server.py"]

