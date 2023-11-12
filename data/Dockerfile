FROM python:3.10

WORKDIR /app

RUN pip install psycopg2 pandas 

# Copy everything in the current directory (which is ./data) to /app in the container
COPY . /app

CMD ["python3", "uploader.py"]