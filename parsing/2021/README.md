# Script para parsear datos de División Territorial

Este proyecto está diseñado para leer datos de un archivo Excel sobre la
división territorial y volcar estos datos en una base de datos MySQL.

## Requisitos

- Python 3.x
- Poetry
- Paquetes de Python:
  - pandas
  - sqlalchemy
  - pymysql
- Archivo Excel con los datos de la división territorial.

## Instalación

1. Clona este repositorio en tu máquina local.
2. Instala los paquetes necesarios utilizando `poetry`:

```bash
poetry install
```

## Uso

### Configuración de Credenciales de Base de Datos

Las credenciales de la base de datos se definen en la clase `DatabaseCreds` en
el archivo de código principal. Puedes editar estos valores según tus
necesidades:

```python
@dataclass
class DatabaseCreds:
    user: str = "root"
    password: str = "admin"
    host: str = "127.0.0.1"
    port: int = 3306
    database: str = "division-territorial-rd"
```

### Ejecución del Script

Para ejecutar el script, asegúrate de que el archivo Excel esté en el mismo
directorio que el script o proporciona la ruta completa al archivo. Luego,
ejecuta el script:

```bash
python nombre_del_script.py
```

El script realizará las siguientes acciones:

1. Leerá y limpiará los datos del archivo Excel.
2. Filtrará los datos según criterios predefinidos.
3. Guardará los datos filtrados en tablas de una base de datos MySQL.
4. Establecerá relaciones entre las tablas mediante claves foráneas.

### Manejo de Errores

El script incluye manejo de errores básico y registrará cualquier error
encontrado durante la ejecución. Si ocurre un error, el script terminará y
mostrará un mensaje de error en la consola.

### Ejemplo de Ejecución

```bash
python parse.py
```
