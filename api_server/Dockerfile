# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code from the correct path
COPY ./api_server/api_server.py .

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]