# Kardinal
_Kardinal_ es una aplicación que permite a sus usuarios tener su propio blog, seguir el de otros usuarios, comentar en sus entradas y tener feeds de entradas.

# Cómo instalar la aplicación localmente
Clonamos el repositorio.
```console
git clone pmaxrod/kardinal
```
Es importante tener [Docker](https://docs.docker.com/engine/install/) instalado.

Entramos en la ruta kardinal/app y ejecutamos
```console
docker compose up -d
```
Esto arrancará los contenedores. Para poblar la base de datos ejecutamos los siguientes comandos.
```console
docker exec -it web python manage.py migrate
docker exec -it web python manage.py loaddata fixtures/initial_data.json
```
Creamos un superusuario para poder [iniciar sesión](http://localhost:8000/admin).
```console
docker exec -it web createsuperuser
```
Entramos en la [interfaz de administración](http://localhost:8000/admin).

Iniciamos sesión con nuestras credenciales.