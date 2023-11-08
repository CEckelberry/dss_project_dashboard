FROM python:3.10

WORKDIR /app

RUN pip install psycopg2 pandas 

COPY ./data /app

CMD ["python3", "uploader.py"]