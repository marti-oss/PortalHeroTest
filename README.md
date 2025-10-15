# PORTAL HERO - Prueba Técnica

## Descripción
> Este repositorio contiene la prueba técnica de `marti-oss` para la start-up Portal Hero.
> Compatible con Python >= 3.10 y PostgreSQL (vía `psycopg2-binary`).

El código propuesto es un deamon que gestiona los procesos de sincronización de productos. 
Hay dos tipos de ficheros de tipo CSV: _feed_ y_feed_ que permiten actualizar el catálogo.
Los ficheros _feed_ sirve para actualizar los productos del catálogo. Con este fichero se añade o actualiza los items del cliente.
Los ficheros _portal_ representan los datos actuales del portal externo. Con este fichero se actualiza la base de datos, añadiendo los productos que no existen, actualizando los existentes y borrando aquellos que no formen parte del fichero.


## Requisitos
Los ficheros deben ser .CSVs. 
Para proceso feed: el nombre del fichero debe contener la palabra feed y no puede contener la palabra portal.
Para procfeso portal: el nombre del fichero debe contener la palabra portal y no puede conter la palabra feed.

La estructura de los ficheros es la siguiente:
Un archivo CSV con las columnas:
+ product_id
+ title
+ price
+ store_id

## Preparar entorno
Este proyecto utiliza Python 3.10+ y requiere la instalación de ciertas dependencias externas.
A continuación se detallan los pasos para crear un entorno virtual y descargar todas las librerías necesarias.
### Dependencias
Las dependecias de esta apliación son:
distlib==0.4.0
filelock==3.20.0
platformdirs==4.5.0
psycopg2-binary==2.9.11
python-dotenv==1.1.1
virtualenv==20.35.3
watchdog==6.0.0
### Crear un entorno virtual
Se recomienda aislar las dependencias mediante un entorno virtual.
En Linux/MacOS:
```
python3 -m venv venv
source venv/bin/activate
```
En Windows (PowerShell)
```
python -m venv venv
.\venv\Scripts\activate
```
### Instalar dependencias
En la raíz del proyecto se encuentra el archivo `requirements.txt`.
Ejecute el siguiente comando para descargar las dependencias:
`pip instal -r requirements.txt`
para verificar la instalación puede ejecutar:
`pip list`
### Crear base de datos PostgreSQL
Crear su propia base de datos SQL y ejecutar el fichero SCHEMA.sql para la cración de la tablas
### Crear variables de entorno
Para configurar la base de datos y el directorio de donde se van a leer los ficheros, se debe crear un fichero `.env` especificando las siguientes variables:
+ PGHOST: host o servidor donde se encuentra la base de datos PostgreSQL
+ PGPORT: El Puerto TCP por el que se conecta PostgreSQL>
+ PGDATABASE Nombre de la base de datos a la que se quiere conectar
+ PGUSER: Usuario con el que se autentica en PostreSQL
+ PGPASSWORD: Contraseña del usuario con el que se autentica en PostgreSQL
+ FOLDER_TO_WATCH: Carpeta a la que apunta el daemon

## Ejecutar programa
Una vez realizado el paso de preparar entorno ejecutar el programa (`python3 main.py`) y añadir los ficheros a procesar en el directorio indicado a la variable de entorno `FOLDER_TO_WATCH`.

Para consultar los log, se autogenera el archivo `program.log` que registra las acciones realizadas.