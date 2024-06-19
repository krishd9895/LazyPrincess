# Use the Python 3.8 slim image as base
FROM python:3.8-slim-buster

# Update and upgrade existing packages
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y git \
    && apt-get clean

# Copy requirements.txt and install dependencies
COPY requirements.txt /requirements.txt
RUN pip install -U pip \
    && pip install -U -r /requirements.txt

# Create a directory for the application
RUN mkdir /LazyPrincess
WORKDIR /LazyPrincess

# Copy your Python application files to the container
COPY . /LazyPrincess

# Set the command to execute your Python script
CMD ["python3", "bot.py"]
