FROM python:trixie AS python-builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update --yes --quiet && apt install --yes --quiet --no-install-recommends \
  build-essential \
  gettext \
  libpq-dev \
  libjpeg62-turbo-dev \
  zlib1g-dev \
  libwebp-dev \
  python3-dev \
  python3-pip \
  gcc \
  musl-dev \
  postgresql \
  postgresql-contrib \
  npm 

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install 'django-tailwind[cookiecutter,honcho,reload]'

# Punto de entrada de PostgreSQL
COPY entrypoint.sh /usr/src/app/entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]
