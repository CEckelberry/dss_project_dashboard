FROM python:3.10

WORKDIR /app

COPY ./downloader_iea/requirements.txt /app
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "main.py"]