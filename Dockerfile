FROM python:3.8

COPY ./requirements.txt /requirements.txt
COPY ./src /web
COPY ./creds.json /secrets/creds.json
COPY ./.env /web/.env
WORKDIR /web

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/py/bin:$PATH"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV GOOGLE_APPLICATION_CREDENTIALS="/secrets/creds.json"
USER django-user

# Gunicorn as app server
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 8 --timeout 0 web.wsgi:application
