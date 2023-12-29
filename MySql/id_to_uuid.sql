-- Se crea función para generar el UUID, en este caso UUIDv4.
-- En caso de poseer una función customizada, solo tiene que remplazar esta.
-- Función extraida de: https://stackoverflow.com/a/32965744/9510988
DELIMITER //

CREATE FUNCTION uuid_v4()
    RETURNS CHAR(36) NO SQL
BEGIN
    -- Generate 8 2-byte strings that we will combine into a UUIDv4
    SET @h1 = LPAD(HEX(FLOOR(RAND() * 0xffff)), 4, '0');
    SET @h2 = LPAD(HEX(FLOOR(RAND() * 0xffff)), 4, '0');
    SET @h3 = LPAD(HEX(FLOOR(RAND() * 0xffff)), 4, '0');
    SET @h6 = LPAD(HEX(FLOOR(RAND() * 0xffff)), 4, '0');
    SET @h7 = LPAD(HEX(FLOOR(RAND() * 0xffff)), 4, '0');
    SET @h8 = LPAD(HEX(FLOOR(RAND() * 0xffff)), 4, '0');

    -- 4th section will start with a 4 indicating the version
    SET @h4 = CONCAT('4', LPAD(HEX(FLOOR(RAND() * 0x0fff)), 3, '0'));

    -- 5th section first half-byte can only be 8, 9 A or B
    SET @h5 = CONCAT(HEX(FLOOR(RAND() * 4 + 8)),
                LPAD(HEX(FLOOR(RAND() * 0x0fff)), 3, '0'));

    -- Build the complete UUID
    RETURN LOWER(CONCAT(
        @h1, @h2, '-', @h3, '-', @h4, '-', @h5, '-', @h6, @h7, @h8
    ));
END
//
-- Switch back the delimiter
DELIMITER ;


-- Agregar columnas UUID a cada tabla y renombrar las claves primarias
ALTER TABLE provincias ADD COLUMN provincia_uuid UUID;
ALTER TABLE municipios ADD COLUMN municipio_uuid UUID;
ALTER TABLE sectores ADD COLUMN sector_uuid UUID;

-- Generar UUIDs para cada fila existente
UPDATE provincias SET provincia_uuid = uuid_v4();
UPDATE municipios SET municipio_uuid = uuid_v4();
UPDATE sectores SET sector_uuid = uuid_v4();

-- Agregar nuevas columnas de clave foránea de UUID a las tablas municipios y sectores
ALTER TABLE municipios ADD COLUMN provincia_uuid UUID;
ALTER TABLE sectores ADD COLUMN municipio_uuid UUID;

-- Actualizar las claves foráneas con los UUID correspondientes
UPDATE municipios SET provincia_uuid = (SELECT provincia_uuid FROM provincias WHERE provincia_id = municipios.provincia_id);
UPDATE sectores SET municipio_uuid = (SELECT municipio_uuid FROM municipios WHERE municipio_id = sectores.municipio_id);

-- Una vez que las relaciones estén establecidas con UUIDs, puedes eliminar las antiguas columnas de clave foránea y cambiar las claves primarias
-- Eliminar las viejas claves foráneas y primarias
ALTER TABLE municipios DROP FOREIGN KEY provincia_id; 
ALTER TABLE sectores DROP FOREIGN KEY municipio_id; 

ALTER TABLE municipios DROP COLUMN provincia_id;
ALTER TABLE sectores DROP COLUMN municipio_id;

ALTER TABLE provincias DROP COLUMN provincia_id;
ALTER TABLE municipios DROP COLUMN municipio_id;
ALTER TABLE sectores DROP COLUMN sector_id;

-- Cambiar las claves primarias
ALTER TABLE provincias ADD PRIMARY KEY (provincia_uuid);
ALTER TABLE municipios ADD PRIMARY KEY (municipio_uuid);
ALTER TABLE sectores ADD PRIMARY KEY (sector_uuid);

-- Establecer las nuevas claves foráneas para usar UUIDs
ALTER TABLE municipios ADD CONSTRAINT fk_provincias FOREIGN KEY (provincia_uuid) REFERENCES provincias (provincia_uuid);
ALTER TABLE sectores ADD CONSTRAINT fk_municipios FOREIGN KEY (municipio_uuid) REFERENCES municipios (municipio_uuid);