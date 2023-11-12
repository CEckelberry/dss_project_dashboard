# Use a Python base image that's known for better compatibility
FROM python:3.8-slim-buster

# Install necessary tools and Chromium with its WebDriver
RUN apt-get update && \
    apt-get install -y wget unzip chromium chromium-driver

# Install Python dependencies
RUN pip install selenium pandas

# Copy the script into the container
COPY . /app/
WORKDIR /app

CMD ["python3", "main.py"]