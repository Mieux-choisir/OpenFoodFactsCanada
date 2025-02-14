# Use an official Python 3 image as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

ENV PYTHONPATH="/app"

COPY requirements.txt .

# Install necessary Python dependencies
RUN pip install --no-cache-dir requests pymongo pandas
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy the current directory contents into the container at /app
COPY scripts/ ./scripts

# Add wait-for-it to wait for MongoDB
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Set command to run Python script after MongoDB is ready
CMD ["/wait-for-it.sh", "mongo:27017", "--", "python", "./scripts/import.py"]
