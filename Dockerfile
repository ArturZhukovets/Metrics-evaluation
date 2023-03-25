FROM python:3.10

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY ./Pipfile ./Pipfile.lock ./

RUN pip install --upgrade pip pipenv

RUN pipenv install --system --deploy --ignore-pipfile

COPY /app .

COPY /.env .

EXPOSE 5000