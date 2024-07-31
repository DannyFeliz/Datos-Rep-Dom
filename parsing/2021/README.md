# Script para parsear datos de División Territorial

Este proyecto está diseñado para leer datos de un archivo de Excel sobre la
división territorial y luego colocar estos datos en una base de datos MySQL.

## Requisitos

- Python 3.x
- Docker (Opcional)
- Poetry
- Paquetes de Python:
  - pandas
  - sqlalchemy
  - pymysql
- Archivo Excel con los datos de la división territorial

## Instalación

1. Clona este repositorio en tu máquina local.
2. Instala los paquetes necesarios utilizando `poetry`:

```bash
poetry install
```

## Uso

### 1. Configuración de Credenciales de Base de Datos

1. Copiar el archivo `.env.example` y nombrarlo `.env`.
2. Modificar los valores de las variables de entorno al gusto.

```sh
cp .env.example .env
vim .env # or can be nano
```

### 2. Ejecutar contenedor de Base de Datos (Opcional)

En dado caso de no tener una base de datos puedes usaer el contenedor de
MySQL/MariaDB que está definido en el archivo `docker-compose.yaml`.

```sh
docker compose up -d
```

### Ejecución del Script

> [!NOTE]\
> Para ejecutar el script, asegúrate de que el archivo de Excel
> (`division_territorial_2021.xlsx`) esté en el mismo directorio que el script.

1. Instalar todas las dependencias del proyecto.
2. Correr el script del archivo `parse.py`.

```bash
poetry install
poetry run python parse.py
```

El script realizará las siguientes acciones:

1. Leerá y limpiará los datos del archivo Excel.
2. Filtrará los datos según criterios predefinidos.
3. Guardará los datos filtrados en tablas de una base de datos MySQL.
4. Establecerá relaciones entre las tablas mediante claves foráneas.
5. Creará un folder llamado `.json_output` y pondrá todos los archivos
   correspondientes para la carpeta `JSON` que son utilizados para MongoDB.
