
DROP TABLE IF EXISTS `barrios`;
CREATE TABLE `barrios` (
  `id` int(11) DEFAULT NULL,
  `nombre` varchar(150) DEFAULT NULL,
  `seccionId` int(11) DEFAULT NULL,
  KEY `ix_barrios_id` (`id`),
  KEY `fk_barrios_secciones` (`seccionId`),
  CONSTRAINT `fk_barrios_secciones` FOREIGN KEY (`seccionId`) REFERENCES `secciones` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;


DROP TABLE IF EXISTS `distritos`;
CREATE TABLE `distritos` (
  `id` int(11) DEFAULT NULL,
  `nombre` varchar(150) DEFAULT NULL,
  `municipioId` int(11) DEFAULT NULL,
  KEY `ix_distritos_id` (`id`),
  KEY `fk_distritos_municipios` (`municipioId`),
  CONSTRAINT `fk_distritos_municipios` FOREIGN KEY (`municipioId`) REFERENCES `municipios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;


DROP TABLE IF EXISTS `municipios`;
CREATE TABLE `municipios` (
  `id` int(11) DEFAULT NULL,
  `provinciaId` int(11) DEFAULT NULL,
  `nombre` varchar(150) DEFAULT NULL,
  KEY `ix_municipios_id` (`id`),
  KEY `fk_municipios_provincias` (`provinciaId`),
  CONSTRAINT `fk_municipios_provincias` FOREIGN KEY (`provinciaId`) REFERENCES `provincias` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;


DROP TABLE IF EXISTS `provincias`;
CREATE TABLE `provincias` (
  `id` int(11) DEFAULT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  KEY `ix_provincias_id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;


DROP TABLE IF EXISTS `secciones`;
CREATE TABLE `secciones` (
  `id` int(11) DEFAULT NULL,
  `nombre` varchar(150) DEFAULT NULL,
  `municipioId` int(11) DEFAULT NULL,
  `distritoId` int(11) DEFAULT NULL,
  KEY `ix_secciones_id` (`id`),
  KEY `fk_secciones_distritos` (`distritoId`),
  KEY `fk_secciones_municipios` (`municipioId`),
  CONSTRAINT `fk_secciones_distritos` FOREIGN KEY (`distritoId`) REFERENCES `distritos` (`id`),
  CONSTRAINT `fk_secciones_municipios` FOREIGN KEY (`municipioId`) REFERENCES `municipios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;


DROP TABLE IF EXISTS `sub_barrios`;
CREATE TABLE `sub_barrios` (
  `id` int(11) DEFAULT NULL,
  `nombre` varchar(150) DEFAULT NULL,
  `barrioId` int(11) DEFAULT NULL,
  KEY `ix_sub_barrios_id` (`id`),
  KEY `fk_sub_barrios_barrios` (`barrioId`),
  CONSTRAINT `fk_sub_barrios_barrios` FOREIGN KEY (`barrioId`) REFERENCES `barrios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_spanish_ci;


-- 2024-07-25 13:51:36
