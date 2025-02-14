# Use an official Python 3 image as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

COPY requirements.txt .

# Install necessary Python dependencies
RUN pip install --no-cache-dir requests pymongo pandas
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copier les scripts Python
COPY scripts/ ./scripts

# Ajouter wait-for-it pour attendre MongoDB
COPY wait-for-it.sh /wait-for-it.sh
RUN chmod +x /wait-for-it.sh

# Définir la commande pour exécuter le script Python après que MongoDB soit prêt
CMD ["/wait-for-it.sh", "mongo:27017", "--", "python", "./scripts/import.py"]