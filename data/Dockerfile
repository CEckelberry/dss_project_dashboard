FROM python:3.10

WORKDIR /app

COPY ./data /app
RUN pip install psycopg2 pandas 

CMD ["python3", "uploader.py"]