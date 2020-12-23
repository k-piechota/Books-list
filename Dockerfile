FROM python:3.7

RUN pip install Flask gunicorn requests flask-mongoengine WTForms

COPY application/ /app

WORKDIR /app

ENV PORT 8081

CMD exec gunicorn --bind :$PORT --workers 1 --timeout 90 --threads 8 app:app
