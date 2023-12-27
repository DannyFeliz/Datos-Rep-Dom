CREATE TABLE `provincias` (
  `provincia_id` tinyint(3) unsigned NOT NULL,
  `provincia` varchar(50) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`provincia_id`),
  UNIQUE KEY `id_UNIQUE` (`provincia_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

CREATE TABLE `municipios` (
  `provincia_id` tinyint(3) unsigned NOT NULL,
  `municipio_id` int(10) unsigned NOT NULL,
  `municipio` varchar(150) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`municipio_id`),
  KEY `provincia_id` (`provincia_id`),
  CONSTRAINT `provincia_id` FOREIGN KEY (`provincia_id`) REFERENCES `provincias` (`provincia_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;

CREATE TABLE `sectores` (
  `municipio_id` int(10) unsigned NOT NULL,
  `sector_id` bigint(20) unsigned NOT NULL,
  `sector` varchar(150) COLLATE utf8_spanish_ci NOT NULL,
  PRIMARY KEY (`sector_id`),
  KEY `ciudad_ir_idx` (`municipio_id`),
  CONSTRAINT `ciudad_ir` FOREIGN KEY (`municipio_id`) REFERENCES `municipios` (`municipio_id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_spanish_ci;
