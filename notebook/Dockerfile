FROM jupyter/scipy-notebook

WORKDIR /app

COPY ./notebook /app
RUN pip install -r requirements.txt

USER root

CMD ["python3 jupyter notebook"]