# Use an official Python 3 image as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

COPY requirements.txt ./

# Install necessary Python dependencies
RUN pip install --no-cache-dir requests pymongo pandas
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at /app
COPY scripts/import.py ./

# Set the command to run your Python script
CMD ["python", "./scripts/import.py"]