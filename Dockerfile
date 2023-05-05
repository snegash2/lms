FROM python:3.9

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /code

COPY requirements.txt ./

RUN poetry install #pip install -r requirements.txt

COPY . /code

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "lms.project.wsgi:application"]
