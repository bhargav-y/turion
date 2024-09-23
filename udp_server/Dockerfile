# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code from the correct path
COPY ./udp_server/udp_server.py .

EXPOSE 5000

# Command to run the UDP server
CMD ["python", "udp_server.py"]