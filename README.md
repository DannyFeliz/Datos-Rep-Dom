# 📝 Datos-Rep-Dom

Este proyecto provee Provincias, Municipios y Sectores de República Dominicana en formato JSON y SQL. La información está actualizada al _27 de junio del 2023_.
## 🧱 Estructura del repositorio
* `JSON/`: contiene los documentos en formato JSON con los datos de las provincias, municipios y sectores. Útil para base de datos NoSQL, como [MongoDB](https://www.mongodb.com/).

* `MySQL/`: contiene los archivos SQL necesarios para crear una base de datos en [MySQL](https://www.mysql.com/)/[MariaDB](https://mariadb.com/) de las provincias, municipios y sectores.

## 🗃️ Importación de la data
### MySQL/MariaDB
```shell
cd MySQL/
mysql -p -u root datos-rep-dom < estructuras_tablas.sql
mysql -p -u root datos-rep-dom < provincias.sql.sql
mysql -p -u root datos-rep-dom < municipios.sql
mysql -p -u root datos-rep-dom < sectores.sql
```

### MongoDB
```shell
cd JSON/
mongoimport -d datos-rep-dom -c provincias provincias.json
mongoimport -d datos-rep-dom -c municipios municipios.json
mongoimport -d datos-rep-dom -c provincias sectores.json
```
