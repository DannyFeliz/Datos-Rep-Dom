# 📝 Datos-Rep-Dom

Este proyecto provee Provincias, Municipios y Sectores de República Dominicana en formato JSON y SQL. La información está actualizada al _27 de junio del 2023_.
## 🧱 Estructura del repositorio
* `JSON/`: contiene los documentos en formato JSON con los datos de las provincias, municipios y sectores. Útil para base de datos NoSQL, como [MongoDB](https://www.mongodb.com/).

* `MySql/`: contiene los archivos SQL necesarios para crear una base de datos en [MySQL](https://www.mysql.com/)/[MariaDB](https://mariadb.com/) de las provincias, municipios y sectores.

## 🗃️ Importación de la data
### MySQL/MariaDB
```shell
cd MySql/
mysql -p -u root datos-rep-dom < estructuras_tablas.sql
mysql -p -u root datos-rep-dom < provincias.sql.sql
mysql -p -u root datos-rep-dom < municipios.sql
mysql -p -u root datos-rep-dom < sectores.sql
```

#### Utilizar UUID en lugar de un número entero como Primary Key
Es posible que prefiera utilizar un [Universally Unique Identifier (UUID)](https://en.wikipedia.org/wiki/Universally_unique_identifier) en lugar de un número entero para no exponer los elementos de la Base de Datos. En ese caso, es posible mediante la utilización del script [`/MySql/id_to_uuid.sql`](/MySql/id_to_uuid.sql), el cual debe de ejecutarse luego de la importación de la data. El script modificará las columnas de la siguiente manera:

| Nombre de la Columna (antiguo) | Nombre de la Columna (nuevo) | Tabla      |
|--------------------------------|------------------------------|------------|
| provincia_id                   | provincia_uuid               | provincias |
| municipio_id                   | municipio_uuid               | municipios |
| sector_id                      | sector_uuid                  | sectores   |

De la misma forma, las llaves foráneas (Foreign Keys) serán renombradas de la siguiente manera.

| Nombre de la Columna (antiguo) | Nombre de la Columna (nuevo) | Tabla      | Columna de referencia | Tabla de referencia |
|--------------------------------|------------------------------|------------|-----------------------|---------------------|
| provincia_id                   | provincia_uuid               | municipios | provincia_uuid        | provincias          |
| municipio_id                   | municipio_uuid               | sectores   | municipio_uuid        | municipios          |


### MongoDB
```shell
cd JSON/
mongoimport -d datos-rep-dom -c provincias provincias.json
mongoimport -d datos-rep-dom -c municipios municipios.json
mongoimport -d datos-rep-dom -c provincias sectores.json
