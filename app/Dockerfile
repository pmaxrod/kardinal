FROM python:trixie AS python-builder

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN apt update --yes --quiet && apt install --yes --quiet --no-install-recommends \
  build-essential npm && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Punto de entrada de PostgreSQL
COPY entrypoint.sh /usr/src/app/entrypoint.sh

ENTRYPOINT ["sh", "./entrypoint.sh"]
