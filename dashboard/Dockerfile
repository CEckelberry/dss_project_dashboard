FROM python:3.10

WORKDIR /app

COPY ./dashboard /app
RUN pip install -r requirements.txt

CMD ["streamlit", "run", "app.py"]
