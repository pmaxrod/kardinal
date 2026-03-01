# Imagen oficial de Python para la versión Trixie de Debian
FROM python:trixie

# Establecer directorio de trabajo
WORKDIR /usr/src/app

# Variabls de entorno
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalación de paquetes
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
  nano \
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
  postgresql-contrib

# Instalación de librerías de Python
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Punto de entrada de PostgreSQL
COPY entrypoint.sh /usr/src/app/entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
